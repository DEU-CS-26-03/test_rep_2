from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import USER_IMAGE_DIR, GARMENT_DIR, RESULT_DIR
from app.services.model_service import model_service
from app.routers import (
    health_router,
    user_image_router,
    garment_router,
    tryon_router,
    result_router,
    model_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_service.initialize()
    print(f"[startup] model status: {model_service.get_status()}")
    yield
    print("[shutdown] cleanup complete")


app = FastAPI(
    title="Virtual Try-On Demo API",
    version="1.0.0",
    description="1차 MVP: 로그인 없는 비동기 가상 피팅 데모 API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files/user-images", StaticFiles(directory=str(USER_IMAGE_DIR)), name="user-images")
app.mount("/files/garments",    StaticFiles(directory=str(GARMENT_DIR)),    name="garments")
app.mount("/files/results",     StaticFiles(directory=str(RESULT_DIR)),     name="results")

app.include_router(health_router.router)
app.include_router(model_router.router)
app.include_router(user_image_router.router)
app.include_router(garment_router.router)
app.include_router(tryon_router.router)
app.include_router(result_router.router)
