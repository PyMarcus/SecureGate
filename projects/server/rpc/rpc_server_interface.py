import typing
from abc import abstractmethod, ABC


class RPCServerInterface(ABC):
    """
    Remote Procedure Call (RPC) is a protocol that one program can use to request
    a service from a program located on another computer in a network without
    having to understand network details.


    With Pyro4, i`ts possible to create distributed applications where Python o
    bjects on different machines can interact seamlessly. Pyro4
    abstracts the complexities of network communication, serialization,
    and deserialization, allowing Python objects to be used remotely
    as if they were local.
    """

    @abstractmethod
    def sing_up(self) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing sing_up method")

    @abstractmethod
    def sign_in(self) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing sing_in method")
