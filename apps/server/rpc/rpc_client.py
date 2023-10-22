import typing

import Pyro4


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

    def sign_up(self, request: typing.Dict[str, typing.Any]) -> bool:
        """
        The sign_up method takes a dictionary as input (request),
        containing user registration information. Specifically, the
        dictionary must include three mandatory fields:

           name: A string representing the user's name.
           email: A string representing the user's email address.
           password: A string representing the user's password.
        """
        return self.client.sign_up(request)
