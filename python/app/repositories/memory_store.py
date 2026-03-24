from typing import Dict, Optional
import threading

class MemoryStore:
    def __init__(self):
        self._lock = threading.Lock()
        self.user_images: Dict[str, dict] = {}
        self.garments: Dict[str, dict] = {}
        self.tryons: Dict[str, dict] = {}
        self.results: Dict[str, dict] = {}

    def save_user_image(self, image_id: str, data: dict):
        with self._lock:
            self.user_images[image_id] = data

    def get_user_image(self, image_id: str) -> Optional[dict]:
        return self.user_images.get(image_id)

    def save_garment(self, garment_id: str, data: dict):
        with self._lock:
            self.garments[garment_id] = data

    def get_garment(self, garment_id: str) -> Optional[dict]:
        return self.garments.get(garment_id)

    def save_tryon(self, tryon_id: str, data: dict):
        with self._lock:
            self.tryons[tryon_id] = data

    def get_tryon(self, tryon_id: str) -> Optional[dict]:
        return self.tryons.get(tryon_id)

    def update_tryon(self, tryon_id: str, updates: dict):
        with self._lock:
            if tryon_id in self.tryons:
                self.tryons[tryon_id].update(updates)

    def get_active_tryon(self) -> Optional[dict]:
        for t in self.tryons.values():
            if t["status"] in ("queued", "processing"):
                return t
        return None

    def save_result(self, result_id: str, data: dict):
        with self._lock:
            self.results[result_id] = data

    def get_result(self, result_id: str) -> Optional[dict]:
        return self.results.get(result_id)

store = MemoryStore()
