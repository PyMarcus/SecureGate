import os

from dotenv import load_dotenv

load_dotenv()


def _map_to_int(value: str | None) -> int | None:
    return int(value) if value is not None else None


class Config:
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


config = Config()
