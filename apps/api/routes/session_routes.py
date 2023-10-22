from fastapi import APIRouter, Depends

from apps.server.rpc.rpc_client import RPCSingletonClient, get_rpc_client

router = APIRouter(
    prefix="/session",
    tags=["session"],
)


@router.get("/signin")
def signin(rpc: RPCSingletonClient = Depends(get_rpc_client)):
    return rpc.sign_in({"email": "securegate@email.com", "password": "notsosecure"})


@router.get("/signup")
def signup(rpc: RPCSingletonClient = Depends(get_rpc_client)):
    return {"message": "signup"}
