from fastapi import APIRouter, Depends

from apps.api.schemas.session_schema import SigninSchema, SignupSchema
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc.rpc_client import RPCSingletonClient, get_rpc_client

routes = APIRouter(
    prefix="/session",
    tags=["session"],
)


@routes.post("/signin")
def signin(body: SigninSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    result = rpc.sign_in(body.model_dump())
    return handle_rpc_result(result)


@routes.post("/signup")
def signup(body: SignupSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    result = rpc.sign_up(body.model_dump())
    return handle_rpc_result(result)
