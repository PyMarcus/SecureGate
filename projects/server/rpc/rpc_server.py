import Pyro4
import typing
import datetime
import threading
from libs import LogMaker, ReadEnv
from projects.server.security import Security
from rpc_server_interface import RPCServerInterface


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

    def __sign_in(self, credentials: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        email: str = credentials["email"]
        password: str = credentials["password"]
        # cosulta do banco retorna senha e user_id pelo email requisitado
        hashed_password: str = "Vai vir do banco."
        user_id: str = "vai vir do banco"
        name: str = "vai vir do banco"
        if not Security.verify_password(hashed_password, password):
            return self.__unauthorizated_message()
        return self.__authorizated_message(name, email, user_id)

    def __sign_up(self, credentials: typing.Dict[str, typing.Any]) -> bool:
        try:
            name: str = credentials["username"]
            email: str = credentials["email"]
            password: str = credentials["password"]
            hashed_password: str = Security.hash_password(password)

            new_user: typing.Dict[str, typing.Any] = {
                "user": name,
                "email": email,
                "hashed_password": hashed_password
            }
            print(new_user)
            return True
        except Exception as err:
            LogMaker.write_log(f"[-] {err}", "error")
            return False

    def __unauthorizated_message(self) -> typing.Dict[str, typing.Any]:
        return {
            "error": "Access to the requested resource is forbidden",
        }

    def __authorizated_message(self, name: str, email: str, user_id: str) -> typing.Dict[str, typing.Any]:
        return {
            "error": None,
            "status": "OK",
            "message": "Welcome!",
            "user_request": name,
            "email": email,
            "time": str(datetime.datetime.now()),
            "user_id": user_id,
            "token": Security.generate_token(user_id)
        }


if __name__ == '__main__':
    re: ReadEnv = ReadEnv("../../../.env.example")
    host: str = re.rpc_host
    port: int = re.rpc_port
    print(f"[+]Running on {host}:{port}")
    daemon: Pyro4.Daemon = Pyro4.Daemon(host=host, port=port)
    LogMaker.write_log(f"[+]RPCServer is running on {host}/{port}", "info")
    server: RPCServer = RPCServer()
    uri: Pyro4.URI = daemon.register(server)
    print(f"[+]URI {uri}")
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
