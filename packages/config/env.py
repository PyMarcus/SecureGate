import os
from os import path

from dotenv import load_dotenv

project_root = path.abspath(path.join(path.dirname(__file__), "../.."))
loaded = load_dotenv(path.join(project_root, ".env"))

print(f"Loaded .env file: {loaded}")


def _map_to_int(value: str | None) -> int | None:
    return int(value) if value is not None else None


class DotEnv:
    """
    Using a .env file in software development is crucial for enhancing security and maintaining flexibility.
    It allows developers to store sensitive information, such as API keys and database credentials,
    separate from the codebase. By keeping these configurations in a separate file, applications become more secure,
    as sensitive data is not hardcoded within the source code. Additionally,
    it simplifies collaboration among developers and deployment processes, ensuring that the same
    codebase can be deployed in various environments without exposing sensitive information.
    Overall, the use of .env files promotes security, flexibility, and best practices in software development.
    """

    # Database
    DATABASE_HOST: str | None = os.getenv("DATABASE_HOST")
    DATABASE_PORT: int | None = _map_to_int(os.getenv("DATABASE_PORT"))
    DATABASE_NAME: str | None = os.getenv("DATABASE_NAME")
    DATABASE_USERNAME: str | None = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD: str | None = os.getenv("DATABASE_PASSWORD")
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    # MQTT
    MQTT_PROTOCOL: str | None = os.getenv("MQTT_PROTOCOL")
    MQTT_HOST: str | None = os.getenv("MQTT_HOST")
    MQTT_PORT: int | None = _map_to_int(os.getenv("MQTT_PORT"))
    MQTT_WS_PORT: int | None = _map_to_int(os.getenv("MQTT_WS_PORT"))
    MQTT_URL: str | None = os.getenv("MQTT_URL")
    MQTT_WS_URL: str | None = os.getenv("MQTT_WS_URL")
    MQTT_USERNAME: str | None = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD: str | None = os.getenv("MQTT_PASSWORD")

    # API
    API_HOST: str | None = os.getenv("API_HOST")
    API_PORT: int | None = _map_to_int(os.getenv("API_PORT"))
    API_VERSION: str | None = os.getenv("API_VERSION")
    API_URL_PREFIX: str | None = os.getenv("API_URL_PREFIX")
    API_URL: str | None = os.getenv("API_URL")

    # RPC
    RPC_HOST: str | None = os.getenv("RPC_HOST")
    RPC_PORT: int | None = _map_to_int(os.getenv("RPC_PORT"))

    # BOARD
    BOARD_AP_SSID: str | None = os.getenv("BOARD_AP_SSID")
    BOARD_AP_PASSWORD: str | None = os.getenv("BOARD_AP_PASSWORD")
    BOARD_TOKEN: str | None = os.getenv("BOARD_TOKEN")

    # BOARD EMULATOR
    BOARD_EMULATOR_HOST: str | None = os.getenv("BOARD_EMULATOR_HOST")
    BOARD_EMULATOR_PORT: int | None = _map_to_int(os.getenv("BOARD_EMULATOR_PORT"))
    BOARD_EMULATOR_URL: str | None = os.getenv("BOARD_EMULATOR_URL")

    # TOKENS
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    FERNET_KEY: str | None = os.getenv("FERNET_KEY")


env = DotEnv()
