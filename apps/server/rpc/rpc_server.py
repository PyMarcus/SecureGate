import base64
import datetime
import threading
import typing
import uuid

import Pyro4
from rpc_server_interface import RPCServerInterface

from apps.server.database import InsertMain, SelectMain
from apps.server.database.models.__all_models import *
from apps.server.rpc.controllers.admin_controller import AdminController
from apps.server.rpc.controllers.session_controller import SessionController
from apps.server.rpc.controllers.user_controller import UserController
from apps.server.security import Security
from libs import LogMaker
from libs.pyro_uri import set_pyro_uri
from packages.config.env import env
from packages.errors.errors import *
from packages.responses.responses import *


def authorization_required(function: typing.Callable) -> typing.Any:
    def wrapper(*args) -> typing.Any:
        LogMaker.write_log(f"[+]Calling {function.__name__}", "info")
        return function(*args)

    return wrapper


@Pyro4.expose
class RPCServer(RPCServerInterface):
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

    __user_logged: uuid.UUID | None = None

    @Pyro4.expose
    def sign_in(self, payload: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return SessionController.sign_in(payload)

    @Pyro4.expose
    def sign_up(self, payload: typing.Dict[str, typing.Any]) -> bool:
        return SessionController.sign_up(payload)

    @Pyro4.expose
    def create_admin(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        return AdminController.create_admin(header, payload)

    @Pyro4.expose
    def create_user(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return UserController.create_user(header, payload)

    @Pyro4.expose
    def register_device(self, device: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__register_device(device)

    @Pyro4.expose
    def register_access_history(
        self, history: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return self.__register_access_history(history)

    @Pyro4.expose
    def select_user(
        self, header: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        return self.__select_user(header, user_id)

    @Pyro4.expose
    def select_member(self, member: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__select_member(member)

    @Pyro4.expose
    def select_device(self, device: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__select_device(device)

    @Pyro4.expose
    def select_access_history(
        self, history: typing.Dict[str, typing.Any], date_ini: str, date_end: str
    ) -> typing.Dict[str, typing.Any]:
        return self.__select_access_history(history, date_ini, date_end)

    @Pyro4.expose
    def decoder(self, device_encrypted: str) -> typing.Dict[str, typing.Any]:
        LogMaker.write_log("[+]calling decoder", "info")
        encrypted_data = base64.urlsafe_b64decode(device_encrypted.get("data"))
        return Security.decrypted_traffic_package(encrypted_data)

    @Pyro4.expose
    def select_all_members(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self.__select_all_members(header)

    @Pyro4.expose
    def select_all_users(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self.__select_all_users(header)

    @Pyro4.expose
    def select_all_devices(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self.__select_all_devices(header)

    @Pyro4.expose
    def select_all_access_history(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self.__select_all_access_history(header)

    @authorization_required
    def __register_device(self, dev: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        if dev.get("email") and dev.get("token"):
            if Security.verify_token(dev.get("email"), dev.get("token")):
                name: str = dev.get("name")
                wifi_ssid: str = dev.get("wifi_ssid")
                version: str = dev.get("version")
                password = Security.hash_password(dev.get("wifi_password"))
                device: Device = Device(
                    name=name, version=version, wifi_ssid=wifi_ssid, wifi_password=password
                )

                if InsertMain.insert_device(device):
                    LogMaker.write_log(f"[+]{device} has been inserted", "info")
                    return True
                LogMaker.write_log(f"[-]Fail to insert {device}", "info")
                return False
        return UnauthorizedError("Invalid token or email").dict()

    @authorization_required
    def __register_access_history(
        self, history: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        if history.get("email") and history.get("token"):
            if Security.verify_token(history.get("email"), history.get("token")):
                history: AccessHistory = AccessHistory(
                    user_id=self.__user_logged,
                    member_id=history.get("member_id"),
                    device_id=history.get("device_id"),
                )
                if InsertMain.insert_access_history(history):
                    LogMaker.write_log(f"[+]{history} has been inserted", "info")
                    return True
                LogMaker.write_log(f"[-]Fail to insert {history}", "info")
                return False
        return UnauthorizedError("Invalid token or email").dict()

    @authorization_required
    def __select_user(
        self, header: typing.Dict[str, str], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        if header.get("email") and header.get("token"):
            if Security.verify_token(header.get("email"), header.get("token")):
                if not user_id:
                    return BadRequestError("User id not found").dict()
                data = SelectMain.select_user_by_id(user_id)
                if data:
                    return OKResponse(
                        message="Successfully selected user",
                        data={
                            "id": str(data.id),
                            "name": data.name,
                            "email": data.email,
                            "role": data.role,
                        },
                    ).dict()
                return NotFoundError("User not found").dict()
            return UnauthorizedError("Invalid token or email").dict()

    @authorization_required
    def __select_device(self, device: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        if device.get("email") and device.get("token"):
            if Security.verify_token(device.get("email"), device.get("token")):
                name: str = device.get("name")
                password: str = device.get("wifi_password")
                device_data: Device = SelectMain.select_device(name)
                if Security.verify_password(device_data.wifi_password, password):
                    if device_data:
                        auth_message = self.__authorized_device_message(
                            str(device_data.id),
                            device_data.name,
                            device_data.wifi_ssid,
                            device_data.version,
                            device_data.wifi_password,
                        )
                        encrypted_data = Security.encrypted_traffic(auth_message)
                        return encrypted_data
                return BadRequestError("Invalid credentials").dict()
        return UnauthorizedError("Invalid token or email").dict()

    @authorization_required
    def __select_member(self, member: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        if member.get("email") and member.get("token"):
            if Security.verify_token(member.get("email"), member.get("token")):
                email: str = member.get("email")
                member_data: Member = SelectMain.select_member(email)
                if member_data:
                    return self.__authorized_member_message(
                        member_data.name,
                        member_data.email,
                        member_data.id,
                        member_data.rfid,
                        member_data.added_by,
                        member_data.authorized,
                    )
                return BadRequestError("Member not found").dict()
        return UnauthorizedError("Invalid token or email").dict()

    @authorization_required
    def __select_access_history(
        self, header: typing.Dict[str, typing.Any], date_ini: str | None, date_end: str | None
    ) -> typing.Dict[str, typing.Any]:
        if header.get("email") and header.get("token"):
            if Security.verify_token(header.get("email"), header.get("token")):
                if date_ini is None and date_end is None:
                    today = datetime.datetime.now()
                    start = datetime.datetime(today.year, today.month, today.day, 6, 0)
                    date_ini = start.strftime("%Y-%m-%d %H:%M")
                    date_end = today.strftime("%Y-%m-%d %H:%M")

                access_data: AccessHistory = SelectMain.select_access_history(date_ini, date_end)
                if access_data:
                    for row in access_data:
                        user = SelectMain.select_user_by_id(row.user_id)
                        member = SelectMain.select_member_by_id(row.member_id)
                        device = SelectMain.select_device_by_id(row.device_id)
                        response = {
                            "id": str(row.id),
                            "member_id": str(member.id),
                            "member_name": member.name,
                            "user_id": str(user.id),
                            "user_name": user.name,
                            "device_id": str(device.id),
                            "device_name": device.name,
                            "when": row.created_at,
                        }
                    return OKResponse(
                        message=f"Successfully selected range {date_ini} to {date_end} of access history",
                        data=response,
                    ).dict()
                return NoContentResponse(message="No data", data={}).dict()
        return UnauthorizedError("Invalid token or email").dict()

    @authorization_required
    def __select_all_users(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        if header.get("email") and header.get("token"):
            if Security.verify_token(header.get("email"), header.get("token")):
                data = SelectMain.select_all_users()
                response: typing.List = list()
                for content in data:
                    response.append(
                        {
                            "name": content.name,
                            "email": content.email,
                            "role": content.role,
                            "root_id": content.root_id,
                            "id": content.id,
                        }
                    )
                return OKResponse(message="Successfully selected all users", data=response).dict()
            return UnauthorizedError("Invalid token or email").dict()
        return BadRequestError("Token or email not found").dict()

    @authorization_required
    def __select_all_members(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        if header.get("email") and header.get("token"):
            if Security.verify_token(header.get("email"), header.get("token")):
                data = SelectMain.select_all_members()
                response: typing.List = list()
                for content in data:
                    response.append(
                        {
                            "name": content.name,
                            "email": content.email,
                            "rfid": content.rfid,
                            "added_by": str(content.added_by),
                            "id": content.id,
                            "authorized": content.authorized,
                        }
                    )
                return OKResponse(message="Successfully selected all members", data=response).dict()
            return UnauthorizedError("Invalid token or email").dict()
        return BadRequestError("Token or email not found").dict()

    @authorization_required
    def __select_all_devices(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        if header.get("email") and header.get("token"):
            if Security.verify_token(header.get("email"), header.get("token")):
                data = SelectMain.select_all_devices()
                response: typing.List = list()
                for content in data:
                    response.append(
                        {
                            "name": content.name,
                            "version": content.version,
                            "id": content.id,
                            "wifi_ssid": content.wifi_ssid,
                        }
                    )
                return OKResponse(message="Successfully selected all devices", data=response).dict()
            return UnauthorizedError("Invalid token or email").dict()
        return BadRequestError("Token or email not found").dict()

    @authorization_required
    def __select_all_access_history(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        if header.get("email") and header.get("token"):
            if Security.verify_token(header.get("email"), header.get("token")):
                access_data: typing.List[AccessHistory] = SelectMain.select_all_access_history()
                if access_data:
                    response: typing.List = list()
                    for row in access_data:
                        user = SelectMain.select_user_by_id(str(row.user_id))
                        member = SelectMain.select_member_by_id(str(row.member_id))
                        device = SelectMain.select_device_by_id(str(row.device_id))
                        response.append(
                            {
                                "id": str(row.id),
                                "member_id": str(member.id),
                                "member_name": member.name,
                                "user_id": str(user.id),
                                "user_name": user.name,
                                "device_id": str(device.id),
                                "device_name": device.name,
                                "when": row.created_at,
                            }
                        )

                    return OKResponse(
                        message="Successfully selected all registers", data=response
                    ).dict()
                return NoContentResponse(message="No data", data={})
            return UnauthorizedError("Invalid token or email").dict()
        return BadRequestError("Token or email not found").dict()

    def __unauthorized_message(self) -> typing.Dict[str, typing.Any]:
        return {"error": "Access to the requested resource is forbidden", "status": 401}

    def __authorized_user_message(
        self, name: str, email: str, user_id: str, role: UserRole
    ) -> typing.Dict[str, typing.Any]:
        return {
            "error": None,
            "status": 200,
            "message": "Welcome!",
            "user_request": name,
            "email": email,
            "time": str(datetime.datetime.now()),
            "user_id": user_id,
            "role": role,
            "token": Security.generate_token(email),
        }

    def __authorized_device_message(
        self,
        id: str,
        name: str,
        wifi_ssid: str,
        version: str,
        password: str,
    ) -> typing.Dict[str, typing.Any]:
        return {
            "error": None,
            "status": 200,
            "message": "It's device",
            "device": name,
            "wifi_ssid": wifi_ssid,
            "version": version,
            "id": id,
            "time": str(datetime.datetime.now()),
            "password": password,
        }

    def __authorized_member_message(
        self,
        name: str,
        email: str,
        member_id: str,
        rfid: str,
        added_by: uuid.UUID,
        authorized: bool,
    ) -> typing.Dict[str, typing.Any]:
        return {
            "error": None,
            "status": 200,
            "message": f"Member {name}",
            "rfid": rfid,
            "added_by": str(added_by),
            "email": email,
            "time": str(datetime.datetime.now()),
            "member_id": member_id,
            "authorized": authorized,
        }

    def __bad_request_message(self) -> typing.Dict[str, typing.Any]:
        return {
            "error": "Bad request",
            "status": 400,
        }


if __name__ == "__main__":
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        raise Exception("RPC_HOST or RPC_PORT not set")
    print(f"[+]Running on {host}:{port}")

    daemon: Pyro4.Daemon = Pyro4.Daemon(host=host, port=port)
    LogMaker.write_log(f"[+]RPCServer is running on {host}/{port}", "info")
    server: RPCServer = RPCServer()
    uri: Pyro4.URI = daemon.register(server)
    set_pyro_uri(uri)
    LogMaker.write_log(f"[+]SERVER URI: {uri}", "info")

    thread: threading.Thread = threading.Thread(target=daemon.requestLoop)
    thread.daemon = True
    thread.start()
    try:
        while True:
            ...
    except KeyboardInterrupt:
        LogMaker.write_log("[-]Server is down", "warning")
        daemon.shutdown()
