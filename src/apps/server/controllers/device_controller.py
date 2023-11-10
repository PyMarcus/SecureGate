import time
import typing
import uuid

from src.packages.database.insert_main import InsertMain
from src.packages.database.select_main import SelectMain
from src.packages.responses.errors import *
from src.packages.logger.logger import Logger
from src.packages.mqtt.mqtt_client import MQTTClient
from src.packages.security import Security
from src.packages.constants.mqtt_topics import MQTTTopic
from src.packages.responses.successes import *
from src.packages.schemas.devices_schema import DeviceActivationSchema, DeviceSchema
from src.packages.schemas.session_header import SessionHeader


logger = Logger("device_controller")

class DeviceController:
    def __init__(self, mqtt_client: MQTTClient):
        self._mqtt = mqtt_client

    def create_device(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = DeviceSchema(**payload)
            if (
                not data.id
                or not data.name
                or not data.wifi_ssid
                or not data.wifi_password
                or not data.version
            ):
                return BadRequestError("Dados inválidos").dict()

            device = Device(
                id=uuid.UUID(data.id),
                name=data.name,
                version=data.version,
                wifi_ssid=data.wifi_ssid,
                wifi_password=Security.hash_password(data.wifi_password),
            )
            print(f"device {device}")
            if InsertMain.insert_device(device):
                logger.info(f"Device {device.name} created")
                return CreatedResponse(message="Dispositivo criado com sucesso!", data=True).dict()
            return InternalServerError("Erro ao criar dispositivo").dict()

        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    def select_device(self, header: typing.Dict[str, typing.Any], device_id: str):
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
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    def select_all_devices(self, header: typing.Dict[str, typing.Any]):
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
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    def select_device_users(self, header: typing.Dict[str, typing.Any], device_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            users = SelectMain.select_users_by_device_id(device_id)
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
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    def handle_device_activation(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, str]
    ):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = DeviceActivationSchema(**payload)
            if not data.device_id or not data.action:
                return BadRequestError("Dados inválidos").dict()

            if data.action.upper() not in ["ACTIVATE", "DEACTIVATE"]:
                return BadRequestError("Ação inválida").dict()

            self._mqtt.publish(MQTTTopic.ACTIVATION.value, json.dumps(payload))
            time.sleep(3)
            return OKResponse(message="Dispositivo ativado com sucesso!", data=True).dict()

        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()
