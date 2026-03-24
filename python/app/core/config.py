from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "workspace" / "uploads"
RESULT_DIR = BASE_DIR / "workspace" / "results"
TEMP_DIR   = BASE_DIR / "workspace" / "temp"
MOCK_DIR   = BASE_DIR / "mock"

USER_IMAGE_DIR = UPLOAD_DIR / "user-images"
GARMENT_DIR    = UPLOAD_DIR / "garments"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE_MB   = 10

USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"

for d in [USER_IMAGE_DIR, GARMENT_DIR, RESULT_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)
