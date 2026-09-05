"""
CONFIG — change settings here, nowhere else in the codebase.
If you switch devices or want to try a different vision model,
this is the only file you should need to touch.
"""

# Which Ollama vision model to use for image description.
# To switch models: run `ollama pull <model_name>` for the new one,
# then just change this string. Nothing else in the code needs to change.
VISION_MODEL = "moondream"

# Alternative models to try if VISION_MODEL underperforms:
#   "llava-phi3"   -> ~2.9GB, stronger but slower on CPU-only machines
#   "llava"        -> larger, only recommended if you move to a machine with a GPU

# Ollama local API address (default install listens here)
OLLAMA_API_URL = "http://localhost:11434"

# OCR settings
OCR_MIN_TEXT_LENGTH = 10  # below this char count, we assume it's an image (X-ray) not text

# Local server settings
HOST = "0.0.0.0"   # 0.0.0.0 lets other devices on the same network reach this server
PORT = 8080

# Storage
DB_FILE = "patient_records.json"
STORAGE_DIR = "patient_files"

# Timeout (seconds) for vision model calls — CPU-only inference can be slow
VISION_MODEL_TIMEOUT = 180
