import base64
import typing

import Pyro4

from apps.server.security import Security
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

    def create_admin(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        return self.client.create_admin(header, payload)

    def create_user(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        """
        The register_member method creates a new member, allowing them access through the gate.
        It takes a dictionary as input (request), containing member registration information.
        The dictionary must include four mandatory fields:
            token: A string representing the users token.
            name: A string representing the member's name.
            email: A string representing the member's email address.
            rfid: A string representing the member's RFID (Radio-Frequency Identification) tag information.
            added_by: A string representing the ID of the person who added this member to the system.
        """
        return self.client.create_user(header, payload)

    def register_access_history(
        self, header: typing.Dict[str, typing.Any], request: typing.Dict[str, typing.Any]
    ) -> bool:
        """
        The register_access_history method creates a new access history.
        It takes a dictionary as input (request), containing member registration information.
        The dictionary must include four mandatory fields:
            token: A string representing the users token.
            email: A string representing the member's email address.
            member_id: A string representing the member's id.
            device_id: A string representing the device's id.
        """
        return self.client.register_access_history(header, request)

    def create_device(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        """
        The register_device method creates a new device, allowing them access through the gate.
        It takes a dictionary as input (request), containing device registration information.
        The dictionary must include four mandatory fields:
            email: A string representing the users's email address.
            token: A string representing the users token.
            name: A string representing the member's name.
            version: A string representing the device's version.
            wifi_ssid: A string representing the wifi's ssid.
            wifi_password: A string representing the wifi's password of device.
        """
        return self.client.create_device(header, payload)

    def select_device_users(
        self, header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        return self.client.select_device_users(header, device_id)

    def select_user(
        self, header: typing.Dict[str, typing.Any], admin_id: str
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_user method get a member with your data
            email: A string representing the users's email address.
            token: A string representing the users token.
        """
        return self.client.select_user(header, admin_id)

    def select_admin(
        self, header: typing.Dict[str, typing.Any], admin_id: str
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_member method get a member with your data
            email: A string representing the member's email address.
            token: A string representing the users token.
        """
        return self.client.select_admin(header, admin_id)

    def select_user_access_history(
        self, header: typing.Dict[str, typing.Any], user_id: str
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_access_history method get a member with your data
            email: A string representing the users's email address.
            token: A string representing the users token.
            date_ini: 2023-10-29 06:00
            date_end: 2023-10-29 18:00

            if no date is passed, the selected data will be that of the current day,
            from 6 am until the time of the search
        """
        return self.client.select_user_access_history(header, user_id)

    def select_all_users_by_device_id(
        self, header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_all_users_by_device_id method get a member with your data
            header:
                email: A string representing the users's email address.
                token: A string representing the users token.

            device_id:
                id of device

        """
        return self.client.select_users_by_device_id(header, device_id)

    def select_device(
        self, header: typing.Dict[str, typing.Any], device_id
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_device method get a device with your data
            email: A string representing the user's email address.
            token: A string representing the token.
            name: A string representing the device's name.
        """
        return self.client.select_device(header, device_id)
        # base64_encoded_data = self.client.select_device(header).get("secure").get("data")
        # encrypted_data = base64.urlsafe_b64decode(base64_encoded_data)
        # return self.client.decoder(encrypted_data)

    def select_all_members(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_members method get a dict list with all members

        header:
            email,
            token
        """
        return self.client.select_all_members(header)

    def select_all_users(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_users method get a dict list with all users

        header:
            email,
            token
        """
        return self.client.select_all_users(header)

    def select_all_devices(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_devices method get a dict list with all devices

        header:
            email,
            token
        """
        return self.client.select_all_devices(header)

    def select_device_access_history(
        self,
        header: typing.Dict[str, str],
        device_id: str,
        date_ini: str | None,
        date_end: str | None,
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_access_history method get a dict list with all access history

        header:
            email,
            token
        """
        return self.client.select_device_access_history(header, device_id, date_ini, date_end)

    def select_device_access_history_by_date(
        self,
        header: typing.Dict[str, str],
        device_id: str,
        date: str | None,
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self.client.select_device_access_history_by_date(header, device_id, date)

    def update_user_authorization(
        self, header: typing.Dict[str, str], request: typing.Dict[str, typing.Any]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The update_user_authorization method update the authorization of user

        header:
            email,
            token

         request:
             user_id: user`s id
             new_authorization: (bool) new authorization value
        """
        return self.client.update_user_authorization(header, request)


def get_rpc_client() -> RPCSingletonClient:
    """
    This function is a factory that returns a RPCSingletonClient
    instance.
    """
    return RPCSingletonClient(uri=get_pyro_uri())


if __name__ == "__main__":
    client: RPCSingletonClient = get_rpc_client()
    """
    print(client.sign_up({
        "name": "root2",
        "email": "imaroot2@email.com",
        "password": "rootsecurity2",
        "role": "root"
    }))
    print(
        client.sign_in(
            {
                "email": "imaroot2@email.com",
                "password": "rootsecurity2",
            }
        )
    )
    print(client.sign_up({
        "name": "admin2",
        "email": "imaadmin@email2.com",
        "password": "adminsecurity2",
    }))
    print(client.sign_up({
        "name": "admin",
        "email": "imaadmin@email.com",
        "password": "adminsecurity",
        "role": "admin"
    }))

    print(
        client.sign_in(
            {
                "email": "imaadmin@email.com",
                "password": "adminsecurity",
            }
        )
    )
    print(
        client.create_user(
            header={"email": "imaadmin@email.com",
                    'token': 'ImltYWFkbWluQGVtYWlsLmNvbSI.ZUPwKA.ermkhm-p1vJqywmOzMLkw_VvhvY',
                    'user_id':'f6c7284b-f5c8-49cb-a219-79aef5d857f3'},
            payload={
                "name": "aluno02",
                "email": "aluno02@email.com",
                "rfid": "40028922ABD",
                "authorized": True,
            }
        )
    )

    header = {"email": "imaadmin@email.com",
              "token": 'ImltYWFkbWluQGVtYWlsLmNvbSI.ZUPwKA.ermkhm-p1vJqywmOzMLkw_VvhvY',
              'user_id':'13daa86d-babd-4fd8-8779-36ca7d052493'}
    print(client.select_all_users(header))

    print(
        client.select_user(
            header,
            'e62d14ac-cd26-4986-ad1f-ea65021f709d'
        )
    )

    """
    data = client.sign_in(
        {
            "email": "imaadmin@email.com",
            "password": "adminsecurity",
        }
    )

    header = {
        "email": data.get("data").get("email"),
        "token": data.get("data").get("token"),
        "user_id": data.get("data").get("user_id"),
    }

    """print(
        client.create_device(
            header,
            {
                "name": "device23333",
                "version": "0.0.0",
                "wifi_ssid": "wifihost",
                "wifi_password": "wifipassword",
            },
        )
    )"""
    print(header)
    r = {"user_id": "eccbe35e-8d4e-4904-8ec8-06d759774984", "new_authorization": False}
    print(r)
    print(client.update_user_authorization(header=header, request=r))
