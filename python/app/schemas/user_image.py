from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserImageResponse(BaseModel):
    image_id: str
    status: str
    view: str
    filename: str
    content_type: Optional[str] = None
    file_url: str
    created_at: datetime
