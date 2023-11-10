import time

from src.apps.device.config.config import config
from src.apps.device.src.services.config_service import ConfigService
from src.apps.device.src.services.wifi_service import WifiService
from src.packages.config.env import env
from src.packages.logger.logger import Logger

logger = Logger("device_boot")


def _boot():
    wifi_service = WifiService()

    if not config.exists():
        config.load_default()

    if config.check():
        wifi_config = config.get("wifi")
        logger.info(f"Connecting to {wifi_config.get('ssid')}...")
        time.sleep(5)
        logger.info("Connected to wifi successfully!")
    else:
        host, port = env.BOARD_API_HOST, env.BOARD_API_PORT
        if not host or not port:
            raise Exception("Missing host or port for emulator")

        config_service = ConfigService(host, port)

        ap_config = config.get("ap")
        wifi_service.host(ap_config.get("ssid"), ap_config.get("password"))

        config_service.start()


_boot()
