from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union
from app.schemas.common import ErrorDetail

class CreateTryonRequest(BaseModel):
    user_image_id: str
    garment_id: str

class TryonCreatedResponse(BaseModel):
    tryon_id: str
    status: str
    message: str
    user_image_id: str
    garment_id: str
    created_at: datetime

class TryonStatusResponse(BaseModel):
    tryon_id: str
    status: str
    progress: int
    user_image_id: str
    garment_id: str
    result_id: Optional[str] = None
    error: Optional[ErrorDetail] = None
    created_at: datetime
    updated_at: datetime
