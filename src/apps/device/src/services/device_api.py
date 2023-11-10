from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.apps.device.config.config import config

device_api = FastAPI(title="SecureGate device config service")
device_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def send_response(status_code: int, success: bool, message: str, data: any = None):
    response = {
        "success": success,
        "status_code": status_code,
        "message": message,
    }
    if data:
        response["data"] = data
    return JSONResponse(status_code=status_code, content=response)


def save_config(payload: dict):
    config.update(payload)
    config_result = config.save_config()
    return config.check_schema(config_result, config.COMPLETE_SCHEMA)


@device_api.post("/")
def configure_device(configuration: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        if token != config.get("token"):
            return send_response(401, False, "Token inválido ou não fornecido")

        if not config.check_schema(configuration, config.CONFIG_SCHEMA):
            return send_response(400, False, "Configuração inválida")

        if save_config(configuration):
            return send_response(
                200,
                True,
                "Configuração salva com sucesso. Reinicie o dispositivo para aplicar as alterações.",
            )

        return send_response(500, False, "Não foi possível salvar a configuração")
    except Exception as e:
        print(e)
        return send_response(500, False, "Não foi possível salvar a configuração")
