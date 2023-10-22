"""
Pode apagar isso dps! SO UM EXEMPLO
"""
import typing
from projects.server.rpc import RPCSingletonClient


client: RPCSingletonClient = RPCSingletonClient(uri="PYRO:obj_73f6cc45416f49cca162cce7f911287b@0.0.0.0:7878")

# cadastrar
payload: typing.Dict[str, typing.Any] = {
    "username": "securegate",
    "email": "securegate@email.com",
    "password": "notsosecure"
}

#response = client.sign_up(request=payload)
#print(response)

# logar
payload: typing.Dict[str, typing.Any] = {
    "email": "securegate@email.com",
    "password": "notsosecure"
}
print(payload)
response = client.sign_in(payload)
print(response)
