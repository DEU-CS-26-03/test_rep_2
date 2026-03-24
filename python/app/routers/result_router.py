from fastapi import APIRouter, HTTPException
from app.schemas.result import ResultResponse
from app.repositories.memory_store import store
from app.core.constants import ErrorCode

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/{result_id}", response_model=ResultResponse)
def get_result(result_id: str):
    data = store.get_result(result_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": ErrorCode.NOT_FOUND, "message": f"Result '{result_id}' not found."}}
        )
    return data
