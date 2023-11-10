import base64
import datetime
import threading
import typing
import uuid
from typing import Any, Dict

import Pyro4
from rpyc import Service
from rpyc.utils.server import ThreadedServer

from apps.server.database import InsertMain
from apps.server.database.models.__all_models import *
from apps.server.mqtt.mqtt_client import MQTTClient
from apps.server.rpc.controllers.access_history_controller import AccessHistoryController
from apps.server.rpc.controllers.admin_controller import AdminController
from apps.server.rpc.controllers.device_controller import DeviceController
from apps.server.rpc.controllers.session_controller import SessionController
from apps.server.rpc.controllers.user_controller import UserController
from apps.server.security import Security
from libs import LogMaker
from packages.config.env import env
from packages.constants.mqtt_topics import MQTTTopic
from packages.errors.errors import *
from packages.schemas.devices_schema import DeviceActivationSchema, RFIDAuthenticationSchema


def authorization_required(function: typing.Callable) -> typing.Any:
    def wrapper(*args) -> typing.Any:
        LogMaker.write_log(f"[+]Calling {function.__name__}", "info")
        return function(*args)

    return wrapper


class RPCServer(Service):
    """
    The SecureGate RPC server offers seamless integration of distributed databases,
    front-end applications, and MQTT messaging, providing a robust solution for interconnected systems.
    By leveraging the Pyro4 library, this server ensures secure and high-performance communication
    between various components of a distributed architecture.

       With SecureGate's RPC server, businesses can effortlessly bridge the gap between their databases,
       user interfaces, and messaging systems. Whether it's updating database records from a remote front-end
       application, delivering real-time notifications through MQTT, or synchronizing data across multiple
       databases, the SecureGate RPC server simplifies complex interactions into streamlined, efficient processes.

       Powered by Pyro4, a trusted Python library, SecureGate's RPC server not only guarantees
       the security of your data transfers but also ensures remarkable performance.
       Pyro4's efficient communication protocols and advanced serialization techniques optimize the exchange
       of data, allowing seamless integration without compromising speed or reliability.

       In essence, SecureGate's RPC server, coupled with Pyro4, offers a secure, high-performance solution
       for businesses seeking distributed systems integration. Whether you're managing databases,
       user interfaces, or messaging services, SecureGate's RPC server provides a reliable foundation for
       building interconnected, efficient, and secure applications
    """

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._setup_mqtt()
        self._subscribe_mqtt_topics()
        self._setup_controllers()

    def _setup_controllers(self):
        self.__device_controller = DeviceController(self._mqtt)

    def _setup_mqtt(self):
        host, port = env.MQTT_HOST, env.MQTT_PORT
        if not host or not port:
            raise Exception("MQTT_HOST or MQTT_PORT not set")

        self._mqtt = MQTTClient(host, port)
        self._mqtt.listen()

    def _subscribe_mqtt_topics(self):
        self._mqtt.subscribe(
            MQTTTopic.AUTHENTICATION.value, self._handle_rfid_authentication_request
        )

    def stop_mqtt(self):
        self._mqtt.stop()

    def on_connect(self, conn):
        message = f"[+]RPCServer is running on {self._host}:{self._port}"
        LogMaker.write_log(message, "info")

    def on_disconnect(self, conn):
        message = "[-]Client disconnected"
        LogMaker.write_log(message, "warning")

    def run(self):
        thread = ThreadedServer(self, hostname=self._host, port=self._port)
        thread.start()

    def exposed_sign_in(
        self, payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        response = SessionController.sign_in(payload)
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
        return self.__device_controller.create_device(header, payload)

    def exposed_register_access_history(  # chamar quando o user passar no portao
        self, header: typing.Dict[str, typing.Any], history: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return self.__register_access_history(header, history)

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
        return self.__device_controller.select_device(header, device_id)

    def exposed_select_device_users(
        self, header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        return self.__device_controller.select_device_users(header, device_id)

    def exposed_select_user_access_history(
        self, header: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        return AccessHistoryController.select_user_access_history(header, user_id)

    def decoder(self, device_encrypted: str) -> typing.Dict[str, typing.Any]:
        LogMaker.write_log("[+]calling decoder", "info")
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
        return self.__device_controller.select_all_devices(header)

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
        return self.__device_controller.handle_device_activation(header, payload)

    def _save_access_history(self, history: AccessHistory) -> bool:
        if InsertMain.insert_access_history(history):
            LogMaker.write_log(f"[+]{history} has been inserted", "info")
            return True
        LogMaker.write_log(f"[-]Fail to insert {history}", "info")
        return False

    def _handle_rfid_authentication_request(self, topic: str, payload: str) -> None:
        try:
            data = RFIDAuthenticationSchema(**json.loads(payload))
            if not data.device_id or not data.rfid:
                raise Exception("Invalid payload")

            user = UserController.authenticate_user_rfid(data.device_id, data.rfid)
            if user:
                if user.authorized:
                    print("User is authorized")

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

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")


if __name__ == "__main__":
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        raise Exception("RPC_HOST or RPC_PORT not set")

    try:
        server = RPCServer(host, port)
        server.run()
    except KeyboardInterrupt:
        server.stop_mqtt()
