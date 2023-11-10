import uvicorn

from apps.emulator.src.services.device_api import device_api
from apps.emulator.src.utils.log import Log
from packages.config.env import env


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
                raise Exception("API_HOST or API_PORT not set")

            uvicorn.run(
                app=device_api,
                host=host,
                port=port,
                log_level="info",
            )
        except KeyboardInterrupt:
            Log.break_()
            Log.danger("Stopping config service")
