from fastapi import APIRouter, Depends, Request

from apps.api.schemas.members_schema import MemberSignUpSchema
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
    token = request.state.token
    print(token)
    return rpc.sign_up(body.model_dump())


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    token = request.state.token
    print(token)
    return rpc.select_all_members()
