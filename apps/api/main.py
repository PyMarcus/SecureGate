from fastapi import Depends, FastAPI

from apps.api.middlewares.auth_middleware import auth_middleware
from apps.api.routes.management_routes import routes as management_routes
from apps.api.routes.session_routes import routes as session_routes
from packages.config.env import env

app = FastAPI(
    title="SecureGate API",
)

app.include_router(management_routes)

app.include_router(session_routes, dependencies=[Depends(auth_middleware)])


app.mount(f"/{env.API_URL_PREFIX}", app)

if __name__ == "__main__":
    import uvicorn

    host, port = env.API_HOST, env.API_PORT
    if not host or not port:
        raise Exception("API_HOST or API_PORT not set")

    uvicorn.run("apps.api.main:app", host=host, port=port, log_level="info")
