from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime, timezone
from app.core.config import USER_IMAGE_DIR
from app.core.constants import ErrorCode
from app.services.file_service import save_upload_file
from app.repositories.memory_store import store
from app.schemas.user_image import UserImageResponse

router = APIRouter(prefix="/user-images", tags=["User Images"])

@router.post("", response_model=UserImageResponse, status_code=201)
async def upload_user_image(
        file: UploadFile = File(...),
        view: str = Form(default="front"),
):
    if view != "front":
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": ErrorCode.BAD_REQUEST, "message": "Only front view is supported."}}
        )

    file_id, save_path = await save_upload_file(file, USER_IMAGE_DIR)
    now = datetime.now(timezone.utc)

    image_data = {
        "image_id": f"usrimg_{file_id}",
        "status": "uploaded",
        "view": view,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_url": f"/files/user-images/{save_path.name}",
        "file_path": str(save_path),
        "created_at": now,
    }
    store.save_user_image(f"usrimg_{file_id}", image_data)
    return image_data


@router.get("/{image_id}", response_model=UserImageResponse)
def get_user_image(image_id: str):
    data = store.get_user_image(image_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": ErrorCode.NOT_FOUND, "message": f"User image '{image_id}' not found."}}
        )
    return data
