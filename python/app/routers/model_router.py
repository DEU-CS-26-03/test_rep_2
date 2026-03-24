from fastapi import APIRouter
from app.services.model_service import model_service
from app.schemas.model_status import ModelStatusResponse

router = APIRouter(tags=["System"])

@router.get("/models/status", response_model=ModelStatusResponse)
def get_model_status():
    return model_service.get_status()
