"""
Pode apagar isso dps! SO UM EXEMPLO
"""
import typing

from apps.server.rpc import RPCSingletonClient

client: RPCSingletonClient = RPCSingletonClient(
    uri="PYRO:obj_59b9167e77ef415ba66dcd6fa57f015b@localhost:7878"
)

# cadastrar
payload: typing.Dict[str, typing.Any] = {
    "username": "securegate213",
    "email": "securegate2@email.com",
    "password": "notsosecure",
}

response = client.sign_up(request=payload)
print(response)

# logar
# payload: typing.Dict[str, typing.Any] = {"email": "securegate@email.com", "password": "notsosecure"}
# print(payload)
# response = client.sign_in(payload)
# print(response)
