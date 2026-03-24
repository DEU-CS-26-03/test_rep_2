from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModelStatusResponse(BaseModel):
    model_name: str
    loaded: bool
    device: str
    busy: bool
    queue_length: int
    last_loaded_at: Optional[datetime] = None
