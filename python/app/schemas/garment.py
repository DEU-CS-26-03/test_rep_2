from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GarmentResponse(BaseModel):
    garment_id: str
    status: str
    category: str
    filename: str
    content_type: Optional[str] = None
    file_url: str
    created_at: datetime
