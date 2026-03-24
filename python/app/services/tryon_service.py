import uuid
import threading
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import RESULT_DIR, MOCK_DIR, USE_MOCK
from app.core.constants import TryonStatus, ErrorCode
from app.repositories.memory_store import store
from app.services.model_service import model_service
from app.schemas.common import ErrorDetail


def _make_id(prefix: str) -> str:
    return f"{prefix}_{str(uuid.uuid4()).replace('-', '')[:8]}"


def create_tryon(user_image_id: str, garment_id: str) -> dict:
    user_img = store.get_user_image(user_image_id)
    if not user_img:
        raise ValueError(f"user_image_id not found: {user_image_id}")

    garment = store.get_garment(garment_id)
    if not garment:
        raise ValueError(f"garment_id not found: {garment_id}")

    if model_service.is_busy:
        raise RuntimeError("BUSY")

    tryon_id = _make_id("tryon")
    now = datetime.now(timezone.utc)

    tryon_data = {
        "tryon_id": tryon_id,
        "status": TryonStatus.QUEUED,
        "progress": 0,
        "user_image_id": user_image_id,
        "garment_id": garment_id,
        "result_id": None,
        "error": None,
        "created_at": now,
        "updated_at": now,
    }
    store.save_tryon(tryon_id, tryon_data)

    thread = threading.Thread(target=_run_inference, args=(tryon_id,), daemon=True)
    thread.start()

    return tryon_data


def _run_inference(tryon_id: str):
    import time

    model_service.set_busy(True)
    now = datetime.now(timezone.utc)

    store.update_tryon(tryon_id, {
        "status": TryonStatus.PROCESSING,
        "progress": 10,
        "updated_at": now,
    })

    try:
        tryon = store.get_tryon(tryon_id)
        user_img = store.get_user_image(tryon["user_image_id"])
        garment  = store.get_garment(tryon["garment_id"])

        user_image_path = Path(user_img["file_path"])
        garment_path    = Path(garment["file_path"])

        result_id   = _make_id("res")
        result_path = RESULT_DIR / f"{result_id}.png"

        store.update_tryon(tryon_id, {"progress": 40, "updated_at": datetime.now(timezone.utc)})

        if USE_MOCK:
            time.sleep(3)
            import shutil
            mock_file = MOCK_DIR / "mock_result.jpg"
            if mock_file.exists():
                shutil.copy(mock_file, result_path)
            else:
                from PIL import Image
                Image.new("RGB", (768, 1024), color=(200, 200, 200)).save(result_path)
        else:
            from vton.catvton_runner import run_catvton
            run_catvton(
                user_image_path=user_image_path,
                garment_path=garment_path,
                output_path=result_path,
            )

        store.update_tryon(tryon_id, {"progress": 90, "updated_at": datetime.now(timezone.utc)})

        result_data = {
            "result_id": result_id,
            "tryon_id": tryon_id,
            "status": "available",
            "result_url": f"/files/results/{result_path.name}",
            "thumbnail_url": None,
            "created_at": datetime.now(timezone.utc),
        }
        store.save_result(result_id, result_data)

        store.update_tryon(tryon_id, {
            "status": TryonStatus.COMPLETED,
            "progress": 100,
            "result_id": result_id,
            "updated_at": datetime.now(timezone.utc),
        })

    except Exception as e:
        store.update_tryon(tryon_id, {
            "status": TryonStatus.FAILED,
            "progress": 100,
            "error": {
                "code": ErrorCode.INFERENCE_FAILED,
                "message": str(e),
            },
            "updated_at": datetime.now(timezone.utc),
        })
    finally:
        model_service.set_busy(False)
