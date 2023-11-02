import typing
import uuid

from apps.server.database import InsertMain, SelectMain
from apps.server.database.models.__all_models import *
from apps.server.security import Security
from libs import LogMaker
from packages.errors.errors import *
from packages.responses.responses import *
from packages.schemas.devices_schema import DeviceSchema
from packages.schemas.session_header import SessionHeader


class DeviceController:
    @staticmethod
    def create_device(header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = DeviceSchema(**payload)
            if not data.name or not data.wifi_ssid or not data.wifi_password or not data.version:
                return BadRequestError("Dados inválidos").dict()

            device = Device(
                id=uuid.uuid4(),
                name=data.name,
                version=data.version,
                wifi_ssid=data.wifi_ssid,
                wifi_password=Security.hash_password(data.wifi_password),
            )
            print(f"device {device}")
            if InsertMain.insert_device(device):
                LogMaker.write_log(f"[+]{device} has been created", "info")
                return CreatedResponse(message="Dispositivo criado com sucesso!", data=True).dict()
            return InternalServerError("Erro ao criar dispositivo").dict()

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_device(header: typing.Dict[str, typing.Any], device_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = SelectMain.select_device(device_id)
            if data:
                return OKResponse(
                    message="Dispositivo encontrado com sucesso!",
                    data={
                        "id": str(data.id),
                        "name": data.name,
                        "wifi_ssid": data.wifi_ssid,
                        "wifi_password": data.wifi_password,
                        "version": data.version,
                    },
                ).dict()
            return NotFoundError("Administrador não encontrado").dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_all_devices(header: typing.Dict[str, typing.Any]):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            devices = SelectMain.select_all_devices()
            response = []
            for d in devices:
                response.append(
                    {
                        "id": d.id,
                        "name": d.name,
                        "version": d.version,
                        "wifi_ssid": d.wifi_ssid,
                    }
                )
            return OKResponse(message="Dispositivos listados com sucesso!", data=response).dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_device_users(header: typing.Dict[str, typing.Any], device_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            users = SelectMain.select_all_users()
            response = []
            for u in users:
                response.append(
                    {
                        "name": u.name,
                        "email": u.email,
                        "rfid": u.rfid,
                        "added_by": str(u.added_by),
                        "id": u.id,
                        "authorized": u.authorized,
                    }
                )
            return OKResponse(message="Usuários listados com sucesso!", data=response).dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()
