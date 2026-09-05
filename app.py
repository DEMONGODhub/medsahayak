"""
LOCAL HOSTING SERVER
---------------------
Wraps the OCR + vision-model pipeline behind a local API endpoint so that:
  - other devices on the same hospital network can send files to be processed
  - if you move this whole setup to a different PC, you just run this same
    script there — nothing about the API changes, only config.py might.

Run with:
    python3 app.py

Then from any device on the same network:
    curl -X POST http://<this-pc-ip>:5000/process \
        -F "patient_id=P001" \
        -F "photo=@photo.jpg" \
        -F "report=@report.jpeg"
"""

import os

from flask import Flask, request, jsonify, render_template

import config
import core

app = Flask(__name__)

UPLOAD_DIR = "uploads_tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    """Serves the upload page — open this in your browser."""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    """Quick check that the server + config are alive."""
    return jsonify({
        "status": "ok",
        "vision_model": config.VISION_MODEL,
    })


@app.route("/process", methods=["POST"])
def process():
    """
    Accepts a patient_id, a photo file, and a report/X-ray image file.
    Runs the full local pipeline and returns the saved record as JSON.
    """
    patient_id = request.form.get("patient_id")
    photo_file = request.files.get("photo")
    report_file = request.files.get("report")

    if not patient_id or not photo_file or not report_file:
        return jsonify({"error": "patient_id, photo, and report are all required"}), 400

    photo_path = os.path.join(UPLOAD_DIR, f"{patient_id}_photo_{photo_file.filename}")
    report_path = os.path.join(UPLOAD_DIR, f"{patient_id}_report_{report_file.filename}")
    photo_file.save(photo_path)
    report_file.save(report_path)

    record = core.process_record(patient_id, photo_path, report_path)

    return jsonify(record)


@app.route("/records", methods=["GET"])
def list_records():
    """Return all stored records — useful for a future management view."""
    return jsonify(core.load_db())


if __name__ == "__main__":
    print(f"Starting local AI server with vision model: {config.VISION_MODEL}")
    app.run(host=config.HOST, port=config.PORT)
