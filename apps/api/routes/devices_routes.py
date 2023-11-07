from fastapi import APIRouter, Depends, Request

from apps.api.utils.get_request_header import get_request_header
from apps.api.utils.handle_rpc_result import handle_rpc_result
from apps.server.rpc import RPCSingletonClient
from apps.server.rpc.rpc_client import get_rpc_client
from packages.schemas.devices_schema import DeviceActivationSchema, DeviceSchema
from packages.schemas.users_schema import CreateUserSchema

routes = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


@routes.post("/")
def create(request: Request, body: DeviceSchema, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.create_device(header, body.model_dump())
    return handle_rpc_result(result)


@routes.get("/")
def get_all(request: Request, rpc: RPCSingletonClient = Depends(get_rpc_client)):
    header = get_request_header(request)
    result = rpc.select_all_devices(header)
    return handle_rpc_result(result)


@routes.get("/{device_id}")
def get_device_by_id(
    request: Request, device_id: str, rpc: RPCSingletonClient = Depends(get_rpc_client)
):
    header = get_request_header(request)
    result = rpc.select_device(header, device_id)
    return handle_rpc_result(result)


@routes.get("/{device_id}/users")
def get_device_users(
    request: Request, device_id: str, rpc: RPCSingletonClient = Depends(get_rpc_client)
):
    header = get_request_header(request)
    result = rpc.select_all_users_by_device_id(header, device_id)
    return handle_rpc_result(result)


@routes.get("/{device_id}/history")
def get_by_device_history(
    request: Request,
    device_id: str,
    date: str | None = None,
    rpc: RPCSingletonClient = Depends(get_rpc_client),
):
    header = get_request_header(request)
    result = rpc.select_device_access_history_by_date(header, device_id, date)
    print(result)
    return handle_rpc_result(result)


@routes.post("/{device_id}/activation")
def activate_device(
    request: Request,
    device_id: str,
    body: DeviceActivationSchema,
    rpc: RPCSingletonClient = Depends(get_rpc_client),
):
    header = get_request_header(request)
    result = rpc.handle_device_activation(header, body.model_dump())
    return handle_rpc_result(result)
