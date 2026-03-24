from datetime import datetime, timezone
from app.core.config import USE_MOCK

class ModelService:
    def __init__(self):
        self._loaded = False
        self._busy = False
        self._queue_length = 0
        self._last_loaded_at = None
        self._device = "cpu"

    def initialize(self):
        if USE_MOCK:
            self._loaded = True
            self._device = "mock"
        else:
            try:
                import torch
                self._device = "cuda" if torch.cuda.is_available() else "cpu"
                self._loaded = True
            except Exception:
                self._loaded = False
        self._last_loaded_at = datetime.now(timezone.utc)

    def get_status(self) -> dict:
        return {
            "model_name": "CatVTON" if not USE_MOCK else "CatVTON (mock)",
            "loaded": self._loaded,
            "device": self._device,
            "busy": self._busy,
            "queue_length": self._queue_length,
            "last_loaded_at": self._last_loaded_at,
        }

    def set_busy(self, busy: bool):
        self._busy = busy

    @property
    def is_loaded(self):
        return self._loaded

    @property
    def is_busy(self):
        return self._busy

model_service = ModelService()
