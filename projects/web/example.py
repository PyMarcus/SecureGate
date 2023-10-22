"""
Pode apagar isso dps! SO UM EXEMPLO
"""
import typing
from projects.server.rpc import RPCSingletonClient


client: RPCSingletonClient = RPCSingletonClient(uri="PYRO:obj_4e89cd274369494c84ccd10af077c44a@0.0.0.0:7878")

# cadastrar
payload: typing.Dict[str, typing.Any] = {
    "username": "securegate",
    "email": "securegate@email.com",
    "password": "notsosecure"
}

response = client.sign_up(request=payload)
print(response)
