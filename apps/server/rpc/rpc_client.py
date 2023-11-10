import typing

import rpyc

from packages.config.env import env


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

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._client: rpyc.core.protocol.Connection = self.connect()

    def connect(self) -> rpyc.core.protocol.Connection:
        return rpyc.connect(
            self._host, self._port, config={"allow_public_attrs": True}, keepalive=True
        )

    def disconnect(self):
        if self._client:
            self._client.close()
        exit(0)

    def sign_in(self, request: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """
        The sign_in method takes a dictionary as input (request),
        containing user registration information. Specifically, the
        dictionary must include two mandatory fields:

           email: A string representing the user's email address.
           password: A string representing the user's password.
        """
        return self._client.root.exposed_sign_in(request)

    def sign_up(self, request: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """
        The sign_up method takes a dictionary as input (request),
        containing user registration information. Specifically, the
        dictionary must include three mandatory fields:

           name: A string representing the user's name.
           email: A string representing the user's email address.
           password: A string representing the user's password.
        """
        return self._client.root.exposed_sign_up(request)

    def create_admin(
        self, header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]
    ) -> bool:
        return self._client.root.exposed_create_admin(header, payload)

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
        return self._client.root.exposed_create_user(header, payload)

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
        return self._client.root.exposed_create_device(header, payload)

    def select_device_users(
        self, header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        return self._client.root.exposed_select_device_users(header, device_id)

    def select_user(
        self, header: typing.Dict[str, typing.Any], admin_id: str
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_user method get a member with your data
            email: A string representing the users's email address.
            token: A string representing the users token.
        """
        return self._client.root.exposed_select_user(header, admin_id)

    def select_admin(
        self, header: typing.Dict[str, typing.Any], admin_id: str
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_member method get a member with your data
            email: A string representing the member's email address.
            token: A string representing the users token.
        """
        return self._client.root.exposed_select_admin(header, admin_id)

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
        return self._client.root.exposed_select_user_access_history(header, user_id)

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
        return self._client.root.exposed_select_users_by_device_id(header, device_id)

    def select_device(
        self, header: typing.Dict[str, typing.Any], device_id
    ) -> typing.Dict[str, typing.Any]:
        """
        The select_device method get a device with your data
            email: A string representing the user's email address.
            token: A string representing the token.
            name: A string representing the device's name.
        """
        return self._client.root.exposed_select_device(header, device_id)
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
        return self._client.root.exposed_select_all_members(header)

    def select_admins_by_root_id(self, header: typing.Dict[str, str], root_id: str):
        return self._client.root.exposed_select_admins_by_root_id(header, root_id)

    def select_all_users(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_users method get a dict list with all users

        header:
            email,
            token
        """
        return self._client.root.exposed_select_all_users(header)

    def select_all_devices(
        self, header: typing.Dict[str, str]
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The select_all_devices method get a dict list with all devices

        header:
            email,
            token
        """
        return self._client.root.exposed_select_all_devices(header)

    def handle_device_activation(
        self, header: typing.Dict[str, str], payload: typing.Dict[str, str]
    ) -> bool:
        """
        The activate_device method activate a device
        """
        return self._client.root.exposed_handle_device_activation(header, payload)

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
        return self._client.root.exposed_select_device_access_history(
            header, device_id, date_ini, date_end
        )

    def select_device_access_history_by_date(
        self,
        header: typing.Dict[str, str],
        device_id: str,
        date: str | None,
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        return self._client.root.exposed_select_device_access_history_by_date(
            header, device_id, date
        )

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
        return self._client.root.exposed_update_user_authorization(header, request)


def get_rpc_client() -> RPCSingletonClient:
    """
    This function is a factory that returns a RPCSingletonClient
    instance.
    """
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        raise Exception("RPC_HOST or RPC_PORT not set")

    return RPCSingletonClient(host, port)


if __name__ == "__main__":
    client: RPCSingletonClient = get_rpc_client()

    data = client.sign_in(
        {
            "email": "imaadmin@email.com",
            "password": "adminsecurity",
        }
    )

    print(data)
