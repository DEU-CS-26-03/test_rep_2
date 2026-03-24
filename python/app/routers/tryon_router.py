from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from app.schemas.tryon import CreateTryonRequest, TryonCreatedResponse, TryonStatusResponse
from app.services import tryon_service
from app.core.constants import ErrorCode
from app.repositories.memory_store import store

router = APIRouter(prefix="/tryons", tags=["Tryons"])

@router.post("", response_model=TryonCreatedResponse, status_code=202)
def create_tryon(req: CreateTryonRequest):
    try:
        tryon_data = tryon_service.create_tryon(req.user_image_id, req.garment_id)
    except RuntimeError as e:
        if "BUSY" in str(e):
            raise HTTPException(
                status_code=409,
                detail={"error": {"code": ErrorCode.TRYON_BUSY, "message": "Another try-on job is currently processing."}}
            )
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": ErrorCode.BAD_REQUEST, "message": str(e)}}
        )

    return {
        "tryon_id": tryon_data["tryon_id"],
        "status": tryon_data["status"],
        "message": "Try-on job created successfully.",
        "user_image_id": tryon_data["user_image_id"],
        "garment_id": tryon_data["garment_id"],
        "created_at": tryon_data["created_at"],
    }


@router.get("/{tryon_id}", response_model=TryonStatusResponse)
def get_tryon_status(tryon_id: str):
    data = store.get_tryon(tryon_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": ErrorCode.NOT_FOUND, "message": f"Tryon job '{tryon_id}' not found."}}
        )
    return data
