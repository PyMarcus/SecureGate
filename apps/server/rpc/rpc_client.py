import typing

import Pyro4

from libs.pyro_uri import get_pyro_uri


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RPCSingletonClient(metaclass=Singleton):
    """
    RPCSingletonClient is a class that implemented as a
    singleton in Python, ensuring that there is only one
    instance of the class throughout the program's execution.
    And this class is a rpc client that needs a uri
    id from server to run.
    """

    def __init__(self, uri: str) -> None:
        """uri example: PYRO:obj_8c60fc357d0d498f9b5112d987024df4@0.0.0.0:1111"""
        self.client = Pyro4.Proxy(uri)

    def sign_in(self, request: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """
        The sign_in method takes a dictionary as input (request),
        containing user registration information. Specifically, the
        dictionary must include two mandatory fields:

           email: A string representing the user's email address.
           password: A string representing the user's password.
        """
        return self.client.sign_in(request)

    def sign_up(self, request: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """
        The sign_up method takes a dictionary as input (request),
        containing user registration information. Specifically, the
        dictionary must include three mandatory fields:

           name: A string representing the user's name.
           email: A string representing the user's email address.
           password: A string representing the user's password.
        """
        return self.client.sign_up(request)

    def register_member(self, request: typing.Dict[str, typing.Any]) -> bool:
        """
        The register_member method creates a new member, allowing them access through the gate.
        It takes a dictionary as input (request), containing member registration information.
        The dictionary must include four mandatory fields:

            name: A string representing the member's name.
            email: A string representing the member's email address.
            rfid: A string representing the member's RFID (Radio-Frequency Identification) tag information.
            added_by: A string representing the ID of the person who added this member to the system.
        """
        return self.client.register_member(request)

    def select_user(self, request: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """
        The select_user method get a member with your data
            email: A string representing the member's email address.
        """
        return self.client.select_user(request)

    def select_member(self, request: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """
        The select_member method get a member with your data
            email: A string representing the member's email address.
        """
        return self.client.select_member(request)

    def select_all_members(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_members method get a dict list with all members
        """
        return self.client.select_all_members()

    def select_all_users(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_users method get a dict list with all users
        """
        return self.client.select_all_users()


def get_rpc_client() -> RPCSingletonClient:
    """
    This function is a factory that returns a RPCSingletonClient
    instance.
    """
    return RPCSingletonClient(uri=get_pyro_uri())


if __name__ == "__main__":
    client: RPCSingletonClient = get_rpc_client()
    """print(client.sign_up({
        "name": "root",
        "email": "imaroot@email.com",
        "password": "rootsecurity",
        "role": "root"
    }))
    print(
        client.sign_in(
            {
                "email": "imaroot@email.com",
                "password": "rootsecurity",
            }
        )
    )
    print(client.sign_up({
        "name": "admin",
        "email": "imaadmin@email.com",
        "password": "adminsecurity",
    }))"""
    """print(
        client.register_member(
            {
                "name": "aluno01",
                "email": "aluno01@email.com",
                "rfid": "40028922ABC",
                "added_by": "0ad91ffb-78dd-4cd3-aeaf-519c7da27b52",
            }
        )
    )
    """
    print(client.select_member({"email": "aluno01@email.com"}))

    print(client.select_user({"email": "imaadmin@email.com"}))

    print(client.select_all_users())
    print(client.select_all_members())
