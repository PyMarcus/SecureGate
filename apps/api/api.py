from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.middlewares.auth_middleware import auth_middleware
from apps.api.middlewares.exception_middleware import exception_middleware
from apps.api.routes.admins_routes import routes as admins_routes
from apps.api.routes.devices_routes import routes as devices_routes
from apps.api.routes.history_routes import routes as history_routes
from apps.api.routes.management_routes import routes as management_routes
from apps.api.routes.session_routes import routes as session_routes
from apps.api.routes.users_routes import routes as users_routes
from packages.config.env import env

app = FastAPI(
    title="SecureGate API",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(management_routes)
app.include_router(session_routes)
app.include_router(devices_routes, dependencies=[Depends(auth_middleware)])
app.include_router(admins_routes, dependencies=[Depends(auth_middleware)])
app.include_router(users_routes, dependencies=[Depends(auth_middleware)])
app.include_router(history_routes, dependencies=[Depends(auth_middleware)])

app.mount(f"/{env.API_URL_PREFIX}", app)

app.add_exception_handler(Exception, exception_middleware)

if __name__ == "__main__":
    from os import path

    import uvicorn

    host, port = env.API_HOST, env.API_PORT
    if not host or not port:
        raise Exception("API_HOST or API_PORT not set")

    project_root = path.abspath(path.join(path.dirname(__file__)))

    uvicorn.run(
        "apps.api.api:app",
        host=host,
        port=port,
        log_level="info",
        reload_dirs=project_root,
        reload=True,
    )
