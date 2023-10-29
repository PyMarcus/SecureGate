from fastapi import APIRouter, Depends, Request

from apps.api.schemas.session_schema import SignupSchema
from apps.api.utils.get_request_header import get_request_header
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client

routes = APIRouter(
    prefix="/users",
    tags=["users"],
)


@routes.post("/")
def create(body: SignupSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    result = rpc.sign_up(body.model_dump())
    return handle_rpc_result(result)


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_all_users(header)
    return handle_rpc_result(result)


@routes.get("/{user_id}")
def get_by_id(request: Request, user_id: str, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_user(header, user_id)
    return handle_rpc_result(result)
