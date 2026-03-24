from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["System"])

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "virtual-tryon-api",
        "time": datetime.now(timezone.utc).isoformat(),
    }
