"""
Pode apagar isso dps!
"""
import typing
from projects.server.rpc import RPCSingletonClient


client: RPCSingletonClient = RPCSingletonClient(uri="PYRO:obj_cb63eb3333ac429a97c28b1782070c62@0.0.0.0:7878")

# cadastrar
payload: typing.Dict[str, typing.Any] = {
    "username": "securegate",
    "email": "securegate@email.com",
    "password": "notsosecure"
}

response = client.sign_up(request=payload)
print(response)
