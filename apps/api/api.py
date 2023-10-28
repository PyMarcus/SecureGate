from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.middlewares.auth_middleware import auth_middleware
from apps.api.routes.management_routes import routes as management_routes
from apps.api.routes.members_routes import routes as members_routes
from apps.api.routes.session_routes import routes as session_routes
from apps.api.routes.users_routes import routes as users_routes
from packages.config.env import env

app = FastAPI(
    title="SecureGate API dfs",
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
app.include_router(users_routes, dependencies=[Depends(auth_middleware)])
app.include_router(members_routes, dependencies=[Depends(auth_middleware)])


app.mount(f"/{env.API_URL_PREFIX}", app)


if __name__ == "__main__":
    import uvicorn

    host, port = env.API_HOST, env.API_PORT
    if not host or not port:
        raise Exception("API_HOST or API_PORT not set")

    uvicorn.run(
        "apps.api.api:app",
        host=host,
        port=port,
        log_level="info",
        reload_dirs=["apps", "libs"],
        reload=True,
    )
