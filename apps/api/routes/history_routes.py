from fastapi import APIRouter, Depends, Request

from apps.api.utils.get_request_header import get_request_header
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client

routes = APIRouter(
    prefix="/history",
    tags=["history"],
)


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_all_access_history(header)
    return handle_rpc_result(result)


@routes.get("/interval/")
def get_by_date(
    request: Request,
    date_ini: str | None = None,
    date_end: str | None = None,
    rpc: RPCSingletonClient = Depends(get_rpc_client),
):
    header = get_request_header(request)
    result = rpc.select_access_history(header, date_ini, date_end)
    return handle_rpc_result(result)
