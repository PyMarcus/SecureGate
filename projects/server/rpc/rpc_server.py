import Pyro4
import typing
import threading
from libs import LogMaker
from rpc_server_interface import RPCServerInterface


class RPCServer(RPCServerInterface):
    def sign_in(self) -> typing.Dict[str, typing.Any]:
        ...

    def sing_up(self) -> typing.Dict[str, typing.Any]:
        ...
