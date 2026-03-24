from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime, timezone
from app.core.config import GARMENT_DIR
from app.core.constants import ErrorCode
from app.services.file_service import save_upload_file
from app.repositories.memory_store import store
from app.schemas.garment import GarmentResponse

router = APIRouter(prefix="/garments", tags=["Garments"])

@router.post("", response_model=GarmentResponse, status_code=201)
async def upload_garment(
        file: UploadFile = File(...),
        category: str = Form(default="top"),
):
    if category != "top":
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": ErrorCode.BAD_REQUEST, "message": "Only 'top' category is supported."}}
        )

    file_id, save_path = await save_upload_file(file, GARMENT_DIR)
    now = datetime.now(timezone.utc)

    garment_data = {
        "garment_id": f"gar_{file_id}",
        "status": "uploaded",
        "category": category,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_url": f"/files/garments/{save_path.name}",
        "file_path": str(save_path),
        "created_at": now,
    }
    store.save_garment(f"gar_{file_id}", garment_data)
    return garment_data


@router.get("/{garment_id}", response_model=GarmentResponse)
def get_garment(garment_id: str):
    data = store.get_garment(garment_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": ErrorCode.NOT_FOUND, "message": f"Garment '{garment_id}' not found."}}
        )
    return data
