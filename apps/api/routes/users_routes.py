from fastapi import APIRouter, Depends, Request

from apps.api.schemas.session_schema import SignupSchema
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client

routes = APIRouter(
    prefix="/users",
    tags=["users"],
)


@routes.post("/")
def create(request: Request, body: SignupSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    token = request.state.token
    print(token)
    return rpc.sign_up(body.model_dump())


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    token = request.state.token
    print(token)
    return rpc.select_all_users()
