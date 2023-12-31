import time

from apps.emulator.config.config import config
from apps.emulator.src.services.config_service import ConfigService
from apps.emulator.src.services.wifi_service import WifiService
from apps.emulator.src.utils.log import Log
from packages.config.env import env


def _boot():
    wifi_service = WifiService()

    if not config.exists():
        config.load_default()

    if config.check():
        wifi_config = config.get("wifi")
        Log.info(f"Connecting to {wifi_config.get('ssid')}...")
        time.sleep(5)
        Log.success("Connected to wifi successfully!")
    else:
        host, port = env.BOARD_API_HOST, env.BOARD_API_PORT
        if not host or not port:
            raise Exception("Missing host or port for emulator")

        config_service = ConfigService(host, port)

        ap_config = config.get("ap")
        wifi_service.host(ap_config.get("ssid"), ap_config.get("password"))

        config_service.start()


_boot()
