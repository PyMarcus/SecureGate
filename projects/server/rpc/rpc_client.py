import Pyro4

# Conectar ao objeto remoto
auth_server = Pyro4.Proxy("PYRO:obj_895ccb6f0a0d4feebc83d6dafa205789@0.0.0.0:7878")

# Autenticar usuário
username = 'marcus'
password = 'senhadomarcus'
user = {"username": username, "password": password}

print(auth_server.sign_up(user))
