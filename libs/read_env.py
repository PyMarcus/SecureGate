import os
from dotenv import load_dotenv


class ReadEnv:
    """
     Using a .env file in software development is crucial for enhancing security and maintaining flexibility.
     It allows developers to store sensitive information, such as API keys and database credentials,
     separate from the codebase. By keeping these configurations in a separate file, applications become more secure,
     as sensitive data is not hardcoded within the source code. Additionally,
     it simplifies collaboration among developers and deployment processes, ensuring that the same
     codebase can be deployed in various environments without exposing sensitive information.
     Overall, the use of .env files promotes security, flexibility, and best practices in software development.
    """
    def __init__(self, path_to_env: str) -> None:
        self.__path_to_env: str = path_to_env
        load_dotenv(self.__path_to_env)
        self.__secret_key: str = os.getenv("SECRET_KEY")
        self.__database_host: str = os.getenv("DATABASE_HOST")
        self.__database_port: int = int(os.getenv("DATABASE_PORT"))
        self.__database_name: str = os.getenv("DATABASE_NAME")
        self.__database_username: str = os.getenv("DATABASE_USERNAME")
        self.__database_password: str = os.getenv("DATABASE_PASSWORD")
        self.__rpc_host: str = os.getenv("HOST")
        self.__rpc_port: int = int(os.getenv("PORT"))


    @property
    def secret_key(self) -> str:
        return self.__secret_key

    @property
    def database_host(self) -> str:
        return self.__database_host

    @property
    def database_port(self) -> int:
        return self.__database_port

    @property
    def database_name(self) -> str:
        return self.__database_name

    @property
    def database_username(self) -> str:
        return self.__database_username

    @property
    def database_password(self) -> str:
        return self.__database_password

    @property
    def rpc_host(self) -> str:
        return self.__rpc_host

    @property
    def rpc_port(self) -> int:
        return self.__rpc_port
