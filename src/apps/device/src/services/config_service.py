import os
import signal
import uvicorn

from src.apps.device.src.services.device_api import device_api
from src.packages.config.env import env
from src.packages.logger.logger import Logger

logger = Logger('device_config_service')


class ConfigService:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def start(self):
        """
        Start the config service.
        """
        host, port = env.BOARD_API_HOST, env.BOARD_API_PORT
        if not host or not port:
            message = "API_HOST or API_PORT not set"
            logger.error(message)
            raise Exception(message)

        uvicorn.run(
            app=device_api,
            host=host,
            port=port,
            log_level="info",
        )

    def stop(self):
        """
        Stop the config service.
        """
        os.kill(os.getpid(), signal.SIGTERM)