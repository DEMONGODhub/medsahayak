"""
CORE PROCESSING — the actual OCR / vision-model / redaction / storage logic.
Reads all tunable settings from config.py so nothing here needs to change
when you swap models or move devices.
"""

import base64
import json
import os
import re
from datetime import datetime, timezone

import pytesseract
import requests
from PIL import Image

import config


def extract_text_with_ocr(image_path):
    """Run Tesseract OCR on the image. Works well for typed/scanned report text."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def describe_with_vision_model(image_path, prompt="Describe any visible medical findings in this image."):
    """
    Call Ollama's local REST API directly (instead of shelling out to the CLI).
    This avoids terminal control-code garbage that leaks in when the `ollama run`
    CLI is captured programmatically, and returns clean JSON instead.
    Which model is used comes entirely from config.VISION_MODEL —
    change that one value to switch models, no code changes needed here.
    """
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        response = requests.post(
            f"{config.OLLAMA_API_URL}/api/generate",
            json={
                "model": config.VISION_MODEL,
                "prompt": prompt,
                "images": [image_b64],
                "stream": False,
            },
            timeout=config.VISION_MODEL_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[vision model error: {e}]"


def redact_pii(text):
    """Local info-blocking step: strip obvious PII before anything leaves this machine."""
    redacted = text
    redacted = re.sub(r"\b\d{6,}\b", "[ID_REDACTED]", redacted)
    redacted = re.sub(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "[DATE_REDACTED]", redacted)
    redacted = re.sub(
        r"(?im)^(patient name|name|dob|date of birth|id number|mrn)\s*:.*$",
        r"\1: [REDACTED]",
        redacted,
    )
    return redacted


def load_db():
    if os.path.exists(config.DB_FILE):
        with open(config.DB_FILE, "r") as f:
            return json.load(f)
    return []


def save_db(records):
    with open(config.DB_FILE, "w") as f:
        json.dump(records, f, indent=2)


def process_record(patient_id, photo_path, report_path):
    """
    Full pipeline for one patient record:
    OCR attempt -> fallback to vision model -> redact -> save -> stage for OpenAI step.
    Returns the saved record as a dict.
    """
    os.makedirs(config.STORAGE_DIR, exist_ok=True)

    raw_ocr_text = extract_text_with_ocr(report_path)

    if len(raw_ocr_text) < config.OCR_MIN_TEXT_LENGTH:
        raw_text = describe_with_vision_model(report_path)
        extraction_method = f"vision_model:{config.VISION_MODEL}"
    else:
        raw_text = raw_ocr_text
        extraction_method = "ocr"

    redacted_text = redact_pii(raw_text)

    record = {
        "patient_id": patient_id,
        "photo_path": photo_path,
        "report_path": report_path,
        "extraction_method": extraction_method,
        "raw_text": raw_text,
        "redacted_text": redacted_text,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "openai_status": "not_sent",
    }

    records = load_db()
    records.append(record)
    save_db(records)

    return record
