import typing
from abc import ABC, abstractmethod


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
    def sign_up(self, payload: typing.Dict[str, typing.Any]) -> bool:
        raise NotImplementedError("missing sing_up method")

    @abstractmethod
    def sign_in(self, payload: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing sing_in method")

    def create_admin(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        raise NotImplementedError("missing create_admin method")

    @abstractmethod
    def create_user(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing register_member method")

    @abstractmethod
    def create_device(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing register_device method")

    @abstractmethod
    def register_access_history(
        self, payload: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing register_access_history method")

    @abstractmethod
    def select_user(
        self, member: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing select_member method")

    @abstractmethod
    def select_admin(
        self, header: typing.Dict[str, typing.Any], admin_id: str
    ) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing select_admin method")

    @abstractmethod
    def select_device(self, device: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing select_device method")

    @abstractmethod
    def select_user_access_history(
        self, header: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("missing select_user_access_history method")

    @abstractmethod
    def select_all_users(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        raise NotImplementedError("missing select_all_members method")

    @abstractmethod
    def select_all_admins(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        raise NotImplementedError("missing select_all_users method")

    @abstractmethod
    def select_all_devices(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        raise NotImplementedError("missing select_all_devices method")

    @abstractmethod
    def select_device_access_history(
        self, header: typing.Dict[str, str], device_id: str
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        raise NotImplementedError("missing select_device_access_history method")
