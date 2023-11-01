from fastapi import APIRouter, Depends, Request

from apps.api.utils.get_request_header import get_request_header
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client
from packages.schemas.users_schema import CreateUserSchema

routes = APIRouter(
    prefix="/users",
    tags=["users"],
)


@routes.post("/")
def create(
    request: Request, body: CreateUserSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)
):
    header = get_request_header(request)
    result = rpc.create_user(header, body.model_dump())
    return handle_rpc_result(result)


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_all_members(header)
    return handle_rpc_result(result)
