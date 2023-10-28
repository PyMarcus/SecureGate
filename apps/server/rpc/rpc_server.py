import datetime
import threading
import typing
import uuid

import Pyro4
from rpc_server_interface import RPCServerInterface

from apps.server.database import InsertMain, SelectMain
from apps.server.database.models.__all_models import *
from apps.server.security import Security
from libs import LogMaker
from libs.pyro_uri import set_pyro_uri
from packages.config.env import env
from packages.errors.errors import BadRequestError, InternalServerError, NotFoundError
from packages.responses.responses import CreatedResponse, OKResponse


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

    @Pyro4.expose
    def sign_in(self, credentials: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__sign_in(credentials)

    @Pyro4.expose
    def sign_up(self, credentials: typing.Dict[str, typing.Any]) -> bool:
        return self.__sign_up(credentials)

    @Pyro4.expose
    def register_member(self, member: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__register_member(member)

    @Pyro4.expose
    def select_user(self, user: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__select_user(user)

    @Pyro4.expose
    def select_member(self, member: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.__select_member(member)

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

    def __sign_in(self, credentials: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        email: str = credentials["email"]
        password: str = credentials["password"]
        user = SelectMain.select_user(email)

        if user is None:
            return NotFoundError("User not found").dict()
        hashed_password: str = user.password
        user_id: str = str(user.id)
        name: str = user.name
        role: UserRole = user.role

        if not Security.verify_password(hashed_password, password):
            return BadRequestError("Invalid Password").dict()
        LogMaker.write_log(f"{user} is logged!", "info")

        return OKResponse(
            message="Successfully signed in",
            data={
                "user_id": user_id,
                "name": name,
                "email": email,
                "token": Security.generate_token(email),
                "role": role,
            },
        ).dict()

    def __sign_up(self, credentials: typing.Dict[str, typing.Any]) -> bool:
        try:
            name: str = credentials["name"]
            email: str = credentials["email"]
            password: str = credentials["password"]
            hashed_password: str = Security.hash_password(password)
            role: UserRole = UserRole.ROOT if credentials.get("role") == "ROOT" else UserRole.ADMIN
            created_uuid: uuid.UUID = uuid.uuid4()
            if role == UserRole.ROOT:
                new_user: User = User(
                    id=created_uuid,
                    name=name,
                    email=email,
                    password=hashed_password,
                    root_id=created_uuid,
                    role=role,
                )
            else:
                root_id = SelectMain.select_root_id()
                new_user: User = User(
                    id=created_uuid,
                    name=name,
                    email=email,
                    password=hashed_password,
                    root_id=root_id,
                    role=role,
                )
            print(new_user.role)
            if InsertMain.insert_user(new_user):
                LogMaker.write_log(f"[+]{new_user} has been inserted", "info")
                return CreatedResponse(message="Successfully signed up", data=True).dict()

            LogMaker.write_log(f"[-]Fail to insert {new_user}", "info")
            return BadRequestError("Fail to insert user").dict()
        except Exception as err:
            LogMaker.write_log(f"[-] {err}", "error")
            return InternalServerError("Internal server error").dict()

    @authorization_required
    def __register_member(
        self, member: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        if member.get("email") and member.get("token"):
            if Security.verify_token(member.get("email"), member.get("token")):
                name: str = member.get("name")
                email: str = member.get("email")
                rfid: str = member.get("rfid")
                authorized: bool = member.get("authorized") if member.get("authorized") else True
                added_by: uuid = member.get("added_by")
                if isinstance(added_by, str):
                    added_by = uuid.UUID(added_by)
                member: Member = Member(
                    name=name, email=email, rfid=rfid, authorized=authorized, added_by=added_by
                )

                if InsertMain.insert_member(member):
                    LogMaker.write_log(f"[+]{member} has been inserted", "info")
                    return True
                LogMaker.write_log(f"[-]Fail to insert {member}", "info")
                return False
        return self.__unauthorized_message()

    @authorization_required
    def __select_user(self, user: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        if user.get("email") and user.get("token"):
            if Security.verify_token(user.get("email"), user.get("token")):
                email: str = user.get("email")
                user_data: User = SelectMain.select_user(email)
                if user_data:
                    return self.__authorized_user_message(
                        user_data.name, user_data.email, str(user_data.id), user_data.role
                    )
                return self.__bad_request_message()
        return self.__unauthorized_message()

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
                return self.__bad_request_message()
        return self.__unauthorized_message()

    @authorization_required
    def __select_all_users(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        if header.get("email") and header.get("token"):
            print(header)
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
                return response
        return self.__unauthorized_message()

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
                return response
        return self.__unauthorized_message()

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
