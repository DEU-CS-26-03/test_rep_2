import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from app.core.constants import ErrorCode

def validate_image_file(file: UploadFile):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": ErrorCode.INVALID_FILE_TYPE,
                    "message": f"Only jpg, jpeg, png are allowed. Got: {ext}"
                }
            }
        )

async def save_upload_file(file: UploadFile, dest_dir: Path) -> tuple[str, Path]:
    validate_image_file(file)
    file_id = str(uuid.uuid4()).replace("-", "")[:12]
    ext = Path(file.filename).suffix.lower()
    save_path = dest_dir / f"{file_id}{ext}"

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": ErrorCode.FILE_TOO_LARGE,
                    "message": f"File size exceeds {MAX_FILE_SIZE_MB}MB limit."
                }
            }
        )

    with open(save_path, "wb") as f:
        f.write(content)

    return file_id, save_path
