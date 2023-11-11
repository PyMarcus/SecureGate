import typing
import uuid
from datetime import datetime

from src.packages.config.env import env
from src.packages.logger.logger import Logger
from termcolor import colored
import rpyc

from src.packages.schemas.admins_schema import AdminSchema
from src.packages.schemas.devices_schema import DeviceSchema
from src.packages.schemas.session_schema import Session, SignupSchema, SigninSchema
from src.packages.schemas.users_schema import CreateUserSchema

logger = Logger("client")


class Client:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._uri = f"{self._host}:{self._port}"
        self._session: Session | None = None
        self._connection: rpyc.Connection | None = None

        self._cmd_prefix = '/'
        self._public_commands = {
            'ajuda': {
                'command': 'ajuda',
                'description': 'Mostra os comandos disponíveis',
                'function': self._help
            },
            'entrar': {
                'command': 'entrar',
                'args': ['email', 'senha'],
                'description': 'Faz login no sistema',
                'function': self._sign_in,
            },
            'cadastrar': {
                'command': 'cadastrar',
                'args': ['nome', 'email', 'senha'],
                'description': 'Cadastra um novo usuário',
                'function': self._sign_up,
            },
        }
        self._private_commands = {
            'sair': {
                'command': 'sair',
                'description': 'Faz logout do sistema',
                'function': self._sign_out,
            },
            'nadmin': {
                'command': 'nadmin',
                'args': ['nome', 'email', 'senha'],
                'description': 'Cria um novo administrador',
                'function': self._create_admin,
            },
            'nusuario': {
                'command': 'nusuario',
                'args': ['nome', 'email', 'rfid', 'id_dispositivo'],
                'description': 'Cria um novo usuário',
                'function': self._create_user,
            },
            'ndispositivo': {
                'command': 'ndispositivo',
                'args': ['nome', 'nome_wifi', 'senha_wifi'],
                'description': 'Cria um novo dispositivo',
                'function': self._create_device,
            },
            'lusuarios': {
                'command': 'lusuarios',
                'args': ['id_dispositivo'],
                'description': 'Lista os usuários de um dispositivo',
                'function': self._list_device_users,
            },
            'luacesso': {
                'command': 'luacesso',
                'args': ['id_usuario'],
                'description': 'Lista o histórico de acesso de um usuário',
                'function': self._list_user_access_history,
            },
            'ladmins': {
                'command': 'ladmins',
                'description': 'Lista os administradores',
                'function': self._list_root_admins,
            },
            'lacesso': {
                'command': 'lacesso',
                'args': ['id_dispositivo'],
                'description': 'Lista o histórico de acesso do dia',
                'function': self._list_day_access_history,
            },
        }

    def _connect(self) -> rpyc.Connection | None:
        try:
            logger.info(f"Conectando em {self._uri}")
            self._connection = rpyc.connect(self._host, self._port,
                                            config={'allow_public_attrs': True})
            return self._connection
        except Exception:
            logger.error(f"Erro ao conectar em {self._uri}")
            return None

    def _disconnect(self) -> None:
        logger.break_()
        logger.info(f"Desconectando de {self._uri}")
        if self._connection:
            self._connection.close()

    def _cli(self) -> None:
        cmd = input(colored('>>> ', 'green')).strip()

        if not cmd.startswith(self._cmd_prefix):
            return logger.error('Comando inválido!')

        args = cmd.split(' ')
        cmd_name, cmd_args = args[0][1:], args[1:]

        private_command = self._private_commands.get(cmd_name)
        public_command = self._public_commands.get(cmd_name)

        if private_command:
            if private_command.get('args') and len(cmd_args) != len(private_command['args']):
                return logger.error('Argumentos inválidos!')
            if not self._session:
                return logger.error('Você precisa estar logado para executar este comando!')
            return private_command['function'](*cmd_args)

        if public_command:
            if public_command.get('args') and len(cmd_args) != len(public_command.get('args')):
                return logger.error('Argumentos inválidos!')
            return public_command['function'](*cmd_args)
        logger.warn('Comando inválido!')

    def run(self) -> None:
        connected = self._connect()
        if connected:
            logger.info('Bem-vindo ao SecureGate!')
            logger.warn('Digite /ajuda para ver os comandos disponíveis')

            self._sign_in('123', '123')  # TODO: remove this, only for testing
            while True:
                try:
                    self._cli()
                except KeyboardInterrupt:
                    self._disconnect()
                    break
        else:
            logger.error('Não foi possível conectar ao servidor')

    # Helpers ======================================================================================
    def _print_commands(self, commands: dict[str, dict]):
        for cmd in commands.values():
            args = f"{' '.join(f'<{arg}>' for arg in cmd['args'])}" if cmd.get('args') else ''
            logger.info(f"{self._cmd_prefix}{cmd['command']} {args} - {cmd['description']}")

    def _print_device_users(self, users: list[dict]):
        if not len(users):
            return logger.info('Nenhum usuário encontrado')
        logger.info('Usuários encontrados:')
        logger.info('Nome - Email - RFID - Autorizado')
        for user in users:
            auth_emoji = '✅' if user['authorized'] else '❌'
            logger.info(f"{user['name']} - {user['email']} - {user['rfid']} - {auth_emoji}")

    def _print_admin_devices(self, devices: list[dict]):
        if not len(devices):
            return logger.info('Nenhum dispositivo encontrado')
        logger.info('Dispositivos encontrados:')
        logger.info('Nome - Nome da rede - Versão')
        for device in devices:
            logger.info(f"{device['name']} - {device['wifi_ssid']} - v{device['version']}")

    def _print_access_history(self, history: list[dict]):
        if not len(history):
            return logger.info('Nenhum histórico de acesso encontrado')
        logger.info('Histórico de acesso encontrado:')
        logger.info('Usuário - Dispositivo - Data')
        for access in history:
            date = datetime.strptime(access['when'], "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%d/%m/%Y %H:%M")
            logger.info(f"{access['user_name']} - {access['device_name']} - {date}")

    def _print_admins(self, admins: list[dict]):
        if not len(admins):
            return logger.info('Nenhum administrador encontrado')
        logger.info('Administradores encontrados:')
        logger.info('ID - Nome - Email')
        for admin in admins:
            logger.info(f"{admin['id']} - {admin['name']} - {admin['email']}")

    # Public =======================================================================================

    def _help(self):
        logger.info('Comandos disponíveis:')
        self._print_commands(self._public_commands)
        if self._session:
            self._print_commands(self._private_commands)

    # Session ======================================================================================
    def _sign_in(self, email: str, password: str):
        try:
            if self._session:
                return logger.error('Você já está logado!')

            payload = SigninSchema(email=email, password=password)
            result = dict(self._connection.root.sign_in(payload.model_dump()))
            if result.get('success'):
                self._session = Session(**result.get('data', {}))
                return logger.success(result.get('message', 'Login realizado com sucesso!'))
            logger.error(result.get('message', 'Erro ao realizar login'))
        except Exception:
            logger.error('Erro ao realizar login')

    def _sign_up(self, name: str, email: str, password: str) -> None:
        try:
            payload = SignupSchema(
                name=name,
                email=email,
                password=password,
                role='ROOT'
            ).model_dump()

            result = dict(self._connection.root.sign_up(payload))
            if result.get('success'):
                return logger.success(result.get('message', 'Usuário cadastrado com sucesso!'))
            logger.error(result.get('message', 'Erro ao cadastrar usuário'))
        except Exception:
            logger.error('Erro ao cadastrar usuário')

    def _sign_out(self):
        self._session = None
        logger.success('Logout realizado com sucesso!')
        self._disconnect()

    # Admin ========================================================================================
    def _create_admin(self, name: str, email: str, password: str) -> None:
        try:
            payload = AdminSchema(
                name=name,
                email=email,
                password=password,
                role='ADMIN',
            ).model_dump()

            result = dict(self._connection.root.create_admin(self._session.model_dump(), payload))
            if result.get('success'):
                return logger.success(result.get('message', 'Administrador criado com sucesso!'))
            logger.error(result.get('message', 'Erro ao criar administrador'))
        except Exception:
            logger.error('Erro ao criar administrador')

    def _list_admin_devices(self, admin_id: str) -> None:
        try:
            result = dict(
                self._connection.root.select_admin_devices(self._session.model_dump(), admin_id))
            if result.get('success'):
                return self._print_admin_devices(result.get('data', []))
            logger.error(result.get('message', 'Erro ao listar dispositivos'))
        except Exception:
            logger.error('Erro ao listar dispositivos')

    def _list_root_admins(self) -> None:
        try:
            if not self._session.role == 'ROOT':
                return logger.error('Você não tem permissão para executar este comando!')

            root_id = self._session.user_id
            result = dict(
                self._connection.root.select_admins_by_root_id(self._session.model_dump(), root_id))
            print(result['data'])
            if result.get('success'):
                return self._print_admins(result.get('data', []))
            logger.error(result.get('message', 'Erro ao listar administradores'))
        except Exception:
            logger.error('Erro ao listar administradores')

    # Device =======================================================================================
    def _create_device(self, name: str, wifi_ssid: str, wifi_password: str) -> None:
        try:
            payload = DeviceSchema(
                id=str(uuid.uuid4()),
                name=name,
                wifi_ssid=wifi_ssid,
                wifi_password=wifi_password,
                version='1.0.0',
            ).model_dump()

            result = dict(self._connection.root.create_device(self._session.model_dump(), payload))
            if result.get('success'):
                return logger.success(result.get('message', 'Dispositivo criado com sucesso!'))
            logger.error(result.get('message', 'Erro ao criar dispositivo'))
        except Exception:
            logger.error('Erro ao criar dispositivo')

    def _list_device_users(self, device_id: str) -> None:
        try:
            result = dict(
                self._connection.root.select_device_users(self._session.model_dump(), device_id))
            if result.get('success'):
                return self._print_device_users(result.get('data', []))
            logger.error(result.get('message', 'Erro ao listar usuários'))
        except Exception:
            logger.error('Erro ao listar usuários')

    # User =========================================================================================
    def _create_user(self, name: str, email: str, rfid: str, device_id: str) -> None:
        try:
            if len(rfid) != 8:
                return logger.error('RFID inválido!')
            payload = CreateUserSchema(
                name=name,
                email=email,
                rfid=rfid,
                authorized=True,
                device_id=device_id,
            ).model_dump()

            result = dict(self._connection.root.create_user(self._session.model_dump(), payload))
            if result.get('success'):
                return logger.success(result.get('message', 'Usuário criado com sucesso!'))
            logger.error(result.get('message', 'Erro ao criar usuário'))
        except Exception:
            logger.error('Erro ao criar usuário')

    def _list_user_access_history(self, user_id: str) -> None:
        try:
            result = dict(
                self._connection.root.select_user_access_history(self._session.model_dump(),
                                                                 user_id))
            if result.get('success'):
                return self._print_access_history(result.get('data', []))
            logger.error(result.get('message', 'Erro ao criar dispositivo'))
        except Exception as e:
            logger.error('Erro ao listar histórico de acesso')

    # Access History ===============================================================================
    def _list_day_access_history(self, device_id: str):
        try:
            today = datetime.utcnow().strftime("%Y-%m-%d")
            result = dict(
                self._connection.root.select_device_access_history_by_date(
                    self._session.model_dump(), device_id, today))

            if result.get('success'):
                return self._print_access_history(result.get('data', []))
            logger.error(result.get('message', 'Erro ao listar histórico de acesso'))
        except Exception:
            logger.error('Erro ao listar histórico de acesso')


if __name__ == "__main__":
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        message = "RPC_HOST or RPC_PORT not set"
        logger.error(message)
        raise Exception(message)

    client = Client(host, port)
    client.run()
