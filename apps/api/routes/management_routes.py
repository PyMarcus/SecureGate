from datetime import datetime

from fastapi import APIRouter

from packages.config.env import env

routes = APIRouter(
    prefix="/management",
    tags=["management"],
)


@routes.get("/health")
def health():
    return {
        "status": "ok",
        "version": env.API_VERSION,
        "time": datetime.now().isoformat(),
    }
