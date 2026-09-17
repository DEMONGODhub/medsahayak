# 🩺 MedSahayak — AI Medical Report Simplifier

> **Making medical reports easier to understand — especially for elderly users.**

MedSahayak is a hackathon project that uses OCR and a local vision model to extract information from medical reports and images, then prepares the content for patient-friendly explanation.

> ⚠️ **Medical safety:** MedSahayak is an information-explanation tool, not a diagnostic system. It must not be used as a substitute for a doctor or qualified healthcare professional.

## ✨ What it does

- 📄 Accepts medical-report images
- 🔎 Extracts text with **Tesseract OCR**
- 👁️ Falls back to a local **Ollama vision model** when OCR is insufficient
- 🔒 Performs a local PII-redaction step before downstream processing
- 💾 Stores processed records locally for development/testing
- 🌐 Exposes a small Flask API and browser upload page
- 🧩 Keeps model/server settings in one configuration file

## 🏗️ Current architecture

```text
Medical report / image
        │
        ▼
     Flask API
        │
        ├── Tesseract OCR
        │       │
        │       └── enough text? ── yes ──► extracted text
        │
        └── no ──► Ollama vision model ──► extracted description
                              │
                              ▼
                       PII redaction
                              │
                              ▼
                    Local JSON record store
```

The current repository uses **local Ollama inference**. A hosted AI/API stage can be added later without changing the basic upload → extraction → redaction flow.

## 📁 Repository structure

```text
medsahayak/
├── app.py                  # Flask API + web server
├── core.py                 # OCR, vision, redaction and storage pipeline
├── config.py               # Model, server and storage settings
├── requirements.txt        # Python dependencies
├── .gitignore              # Local/runtime files excluded from Git
├── templates/
│   └── index.html          # Browser interface
├── static/                 # Frontend assets, if present
├── patient_files/          # Runtime patient files (not for Git)
├── uploads_tmp/            # Temporary uploads (not for Git)
└── README.md
```

The repository also contains hackathon presentation documents and earlier project archives.

## 🚀 Quick start

### 1. Clone

```bash
git clone https://github.com/DEMONGODhub/medsahayak.git
cd medsahayak
```

### 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install system dependencies

MedSahayak uses Tesseract through `pytesseract`, so **Tesseract OCR must also be installed on the operating system**.

On Debian/Ubuntu/Linux Mint:

```bash
sudo apt update
sudo apt install tesseract-ocr
```

Install and start [Ollama](https://ollama.com/), then pull the configured vision model:

```bash
ollama pull moondream
```

### 5. Run

```bash
python app.py
```

Open the local address shown by Flask in your browser.

The API health endpoint is:

```text
GET /health
```

The processing endpoint expects:

```text
POST /process
```

with `patient_id`, `photo`, and `report` form fields.

## ⚙️ Configuration

Edit `config.py` to change the local vision model, Ollama URL, OCR threshold, server port, storage locations, or model timeout.

Current defaults include:

```python
VISION_MODEL = "moondream"
OLLAMA_API_URL = "http://localhost:11434"
HOST = "0.0.0.0"
PORT = 8080
```

For a different Ollama vision model, pull the model first and then update `VISION_MODEL`.

## 🔐 Privacy & security

This project handles **potentially sensitive medical information**. During development:

- Use synthetic, public, or properly redacted test reports.
- Never commit real patient records, patient photos, medical reports, or API credentials.
- Keep runtime folders such as `patient_files/` and `uploads_tmp/` outside Git.
- Treat `patient_records.json` as local development data, not source code.
- Do not expose the Flask server to the public internet without adding authentication, authorization, secure transport, input validation, and appropriate data-protection controls.
- PII redaction is heuristic and **must not be treated as a guarantee of anonymization**.

### Medical disclaimer

MedSahayak explains medical-report language for educational/informational use. It does **not** diagnose disease, prescribe treatment, or replace professional medical advice. Users should discuss medical reports and concerning symptoms with a qualified healthcare professional.

## 🧠 AI behavior goals

The explanation layer should:

- Prefer plain language over unnecessary medical jargon.
- Explain terminology rather than inventing conclusions.
- Clearly separate reported findings from interpretation.
- Avoid diagnosis and treatment recommendations.
- State uncertainty when the source report is unclear.
- Encourage discussion with a healthcare professional when appropriate.

## 🛣️ Roadmap

- [x] Project concept and architecture
- [x] Local OCR + vision-model pipeline
- [x] Local PII-redaction stage
- [x] Flask API
- [ ] Improve file validation and safe temporary-file handling
- [ ] Add automated tests
- [ ] Add structured API error handling
- [ ] Improve frontend accessibility
- [ ] Add a dedicated explanation layer
- [ ] Add authentication before network deployment
- [ ] Add privacy-safe database/storage design
- [ ] Add optional hosted AI integration
- [ ] Prepare final hackathon demo

## 👥 Team areas

| Area | Responsibility |
|---|---|
| 🤖 Local AI | Vision/OCR model and extraction |
| ⚙️ Backend/API | Flask server and integrations |
| 🧠 Prompt Engineering | Patient-friendly explanations |
| 🎨 Frontend/UI | Upload and results experience |
| 🔒 Data & Privacy | Safe test data and privacy checks |
| 🎤 Presentation | Demo, slides and pitch |

## 🤝 Contributing

For development changes:

1. Create a feature branch.
2. Make a focused change.
3. Run the application and relevant tests.
4. Do not include real patient data.
5. Open a pull request with a clear description of the change.

## 📜 License

No open-source license is currently specified. Until a license is added, the default copyright rules apply and others should not assume they have permission to reuse the code.

## 📌 Project

**MedSahayak — AI Medical Report Simplifier**  
Hackathon project — 2026
