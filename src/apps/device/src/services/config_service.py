import uvicorn

from apps.emulator.src.services.device_api import device_api
from src.packages.config.env import env
from src.packages.logger.Logger import Logger

logger = Logger('device_config_service')


class ConfigService:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def start(self):
        """
        Start the config service.
        """
        try:
            host, port = env.BOARD_API_HOST, env.BOARD_API_PORT
            if not host or not port:
                message = "API_HOST or API_PORT not set"
                logger.danger(message)
                raise Exception(message)

            uvicorn.run(
                app=device_api,
                host=host,
                port=port,
                log_level="info",
            )
        except KeyboardInterrupt:
            logger.danger("Stopping config service")
