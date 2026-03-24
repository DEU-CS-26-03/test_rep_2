from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResultResponse(BaseModel):
    result_id: str
    tryon_id: str
    status: str
    result_url: str
    thumbnail_url: Optional[str] = None
    created_at: datetime
