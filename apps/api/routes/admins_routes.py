from fastapi import APIRouter, Depends, Request

from apps.api.utils.get_request_header import get_request_header
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client
from packages.schemas.admins_schema import AdminSchema
from packages.schemas.session_schema import SignupSchema

routes = APIRouter(
    prefix="/admins",
    tags=["admins"],
)


@routes.post("/")
def create(request: Request, body: AdminSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.create_admin(header, body.model_dump())
    return handle_rpc_result(result)


@routes.get("/{root_id}")
def get_all_by_root_id(
    request: Request, root_id: str, rpc: RPCSingletonClient = Depends(get_rpc_client)
):
    header = get_request_header(request)
    result = rpc.select_admins_by_root_id(header, root_id)
    return handle_rpc_result(result)


@routes.get("/{admin_id}")
def get_by_id(request: Request, admin_id: str, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_admin(header, admin_id)
    return handle_rpc_result(result)
