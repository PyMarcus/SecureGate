from fastapi import FastAPI

from apps.api.routes.session_routes import router as session_router
from packages.config.env import env

app = FastAPI()

app.include_router(session_router)

if __name__ == "__main__":
    import uvicorn

    host, port = env.API_HOST, env.API_PORT
    if not host or not port:
        raise Exception("API_HOST or API_PORT not set")

    uvicorn.run("apps.api.main:app", host=host, port=port)
