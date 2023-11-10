import base64
import typing
import uuid

from src.apps.server.controllers.access_history_controller import AccessHistoryController
from src.apps.server.controllers.admin_controller import AdminController
from src.apps.server.controllers.device_controller import DeviceController
from src.apps.server.controllers.session_controller import SessionController
from src.apps.server.controllers.user_controller import UserController
from src.packages.config.env import env
import json
from rpyc import Service
from rpyc.utils.server import ThreadedServer

from src.packages.constants.mqtt_topics import MQTTTopic
from src.packages.database.insert_main import InsertMain
from src.packages.database.models.access_history import AccessHistory
from src.packages.logger.Logger import Logger
from src.packages.mqtt.mqtt_client import MQTTClient
from src.packages.schemas.devices_schema import RFIDAuthenticationSchema, DeviceActivationSchema
from src.packages.security import Security

logger = Logger("server")


class Server(Service):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

        self._setup_mqtt()
        self._subscribe_mqtt_topics()
        self._setup_controller()

    def _setup_mqtt(self) -> None:
        host, port = env.MQTT_HOST, env.MQTT_PORT
        if not host or not port:
            message = "MQTT_HOST or MQTT_PORT not set"
            logger.danger(message)
            raise Exception(message)

        self._mqtt = MQTTClient(host, port)
        self._mqtt.listen()

    def _subscribe_mqtt_topics(self) -> None:
        self._mqtt.subscribe(MQTTTopic.AUTHENTICATION.value, self._handle_rfid_auth)

    def stop_mqtt(self):
        self._mqtt.stop()

    def _setup_controller(self) -> None:
        self._device_controller = DeviceController(self._mqtt)

    def on_connect(self, conn):
        logger.info(f"New connection: {conn}")

    def on_disconnect(self, conn):
        logger.info(f"Disconnected: {conn}")

    def run(self) -> None:
        thread = ThreadedServer(self, hostname=self._host, port=self._port)
        thread.start()

    def exposed_sign_in(self, payload: typing.Dict[str, typing.Any]) -> typing.Dict[
        str, typing.Any]:
        response = SessionController.sign_in(payload)
        self.__user_logged = response.get("data").get("user_id")
        return response

    def exposed_sign_up(self, payload: typing.Dict[str, typing.Any]) -> bool:
        return SessionController.sign_up(payload)

    def exposed_create_admin(
            self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        return AdminController.create_admin(header, payload)

    def exposed_create_user(
            self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return UserController.create_user(header, payload)

    def exposed_create_device(
            self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return self._device_controller.create_device(header, payload)

    def exposed_register_access_history(  # chamar quando o user passar no portao
            self, header: typing.Dict[str, typing.Any], history: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return self._register_access_history(header, history)

    def exposed_select_admin(
            self, header: typing.Dict[str, typing.Any], admin_id: str
    ) -> typing.Dict[str, typing.Any]:
        return AdminController.select_admin(header, admin_id)

    def exposed_select_user(
            self, header: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        return UserController.select_user(header, user_id)

    def exposed_select_device(
            self, header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        return self._device_controller.select_device(header, device_id)

    def exposed_select_device_users(
            self, header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        return self._device_controller.select_device_users(header, device_id)

    def exposed_select_user_access_history(
            self, header: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        return AccessHistoryController.select_user_access_history(header, user_id)

    def exposed_decoder(self, device_encrypted: str) -> typing.Dict[str, typing.Any]:
        logger.info("calling decoder")
        encrypted_data = base64.urlsafe_b64decode(device_encrypted.get("data"))
        return Security.decrypted_traffic_package(encrypted_data)

    def exposed_select_all_users(
            self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return UserController.select_all_users(header)

    def exposed_select_admins_by_root_id(
            self, header: typing.Dict[str, str], root_id: str
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return AdminController.select_admins_by_root_id(header, root_id)

    def exposed_select_all_devices(
            self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self._device_controller.select_all_devices(header)

    def exposed_select_users_by_device_id(
            self,
            header: typing.Dict[str, str],
            device_id: str,
    ) -> dict[str, Any]:
        return UserController.select_users_by_device_id(header=header, device_id=device_id)

    def exposed_select_device_access_history(
            self,
            header: typing.Dict[str, str],
            device_id: str,
            date_ini: str | None,
            date_end: str | None,
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return AccessHistoryController.select_device_access_history(
            header, device_id, date_ini, date_end
        )

    def exposed_select_device_access_history_by_date(
            self, header: typing.Dict[str, str], device_id: str, date: str
    ):
        return AccessHistoryController.select_device_access_history_by_date(header, device_id, date)

    def exposed_update_user_authorization(
            self, header: typing.Dict[str, str], user: typing.Dict[str, typing.Any]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return UserController.update_user_authorization(header, user)

    def exposed_handle_device_activation(
            self, header: typing.Dict[str, str], payload: typing.Dict[str, str]
    ) -> bool:
        return self._device_controller.handle_device_activation(header, payload)

    def _save_access_history(self, history: AccessHistory) -> bool:
        if InsertMain.insert_access_history(history):
            logger.info(f"{history} has been inserted")
            return True
        logger.info(f"Fail to insert {history}")
        return False

    def _handle_rfid_auth(self, topic: str, payload: str) -> None:
        try:
            data = RFIDAuthenticationSchema(**json.loads(payload))
            if not data.device_id or not data.rfid:
                raise Exception("Invalid payload")

            user = UserController.authenticate_user_rfid(data.device_id, data.rfid)
            if user:
                if user.authorized:
                    logger.info(f"User {user.id} authenticated")
                    activation_payload = DeviceActivationSchema(
                        device_id=str(user.device_id),
                        action="ACTIVATE",
                    ).model_dump()

                    self._mqtt.publish(MQTTTopic.ACTIVATION.value, json.dumps(activation_payload))

                    history: AccessHistory = AccessHistory(
                        id=uuid.uuid4(),
                        user_id=user.id,
                        admin_id=None,
                        device_id=user.device_id,
                    )
                    self._save_access_history(history)
                else:
                    logger.info(f"User {user.id} not authorized")

        except Exception as e:
            logger.danger(str(e))


if __name__ == "__main__":
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        message = "RPC_HOST or RPC_PORT not set"
        logger.danger(message)
        raise Exception(message)

    try:
        server = Server(host, port)
        server.run()
    except Exception as e:
        logger.danger(str(e))
        exit(1)
    except KeyboardInterrupt:
        logger.info("Shutting down server")
        server.stop_mqtt()
        exit(0)
