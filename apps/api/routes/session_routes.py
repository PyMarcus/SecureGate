from fastapi import APIRouter, Depends

from apps.api.schemas.session_schema import SigninSchema, SignupSchema
from apps.server.rpc.rpc_client import RPCSingletonClient, get_rpc_client

routes = APIRouter(
    prefix="/session",
    tags=["session"],
)


@routes.post("/signin")
def signin(body: SigninSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    result = rpc.sign_in(body.model_dump())
    return result


@routes.post("/signup")
def signup(body: SignupSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    print(f"data: {body.model_dump()}")
    result = rpc.sign_up(body.model_dump())
    print(result)
    return result
