from fastapi import APIRouter, Depends, Request

from apps.api.schemas.members_schema import MemberSignUpSchema
from apps.api.utils.get_request_header import get_request_header
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client

routes = APIRouter(
    prefix="/members",
    tags=["members"],
)


@routes.post("/")
def create(
    request: Request, body: MemberSignUpSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)
):
    header = get_request_header(request)
    print(header)
    result = rpc.sign_up(body.model_dump())
    handle_rpc_result(result)


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_all_members(header)
    return handle_rpc_result(result)