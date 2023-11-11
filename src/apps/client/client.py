import typing

from src.packages.config.env import env
from src.packages.logger.logger import Logger
from termcolor import colored
import rpyc

from src.packages.schemas.session_schema import Session, SignupSchema, SigninSchema

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

            while True:
                try:
                    self._cli()
                except KeyboardInterrupt:
                    self._disconnect()
                    break
        else:
            logger.error('Não foi possível conectar ao servidor')

    # Public =======================================================================================
    def _print_commands(self, commands: dict[str, dict]):
        for cmd in commands.values():
            args = f"{' '.join(f'<{arg}>' for arg in cmd['args'])}" if cmd.get('args') else ''
            logger.info(f"{self._cmd_prefix}{cmd['command']} {args} - {cmd['description']}")

    def _help(self):
        logger.info('Comandos disponíveis:')
        self._print_commands(self._public_commands)
        if self._session:
            self._print_commands(self._private_commands)

    # Session ======================================================================================
    def _sign_in(self, email: str, password: str):
        payload = SigninSchema(email=email, password=password)
        try:
            result = dict(self._connection.root.sign_in(payload.model_dump()))
            if result.get('success'):
                print(result.get('data'))
                logger.success(result.get('message', 'Login realizado com sucesso!'))
            else:
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
                logger.success(result.get('message', 'Usuário cadastrado com sucesso!'))
            else:
                logger.error(result.get('message', 'Erro ao cadastrar usuário'))
        except Exception:
            logger.error('Erro ao cadastrar usuário')

    def _sign_out(self):
        pass

    # Admin ========================================================================================

    # Device =======================================================================================

    # User =========================================================================================

    # Access History ===============================================================================


if __name__ == "__main__":
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        message = "RPC_HOST or RPC_PORT not set"
        logger.error(message)
        raise Exception(message)

    client = Client(host, port)
    client.run()
