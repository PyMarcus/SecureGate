from apps.emulator.config.config import config
from apps.emulator.src.services.wifi_service import WifiService


def _boot():
    wifi_service = WifiService()

    if not config.exists():
        config.load_default()

    if config.check():
        wifi_config = config.get("wifi")
        print(wifi_config)
    else:
        ap_config = config.get("ap")
        wifi_service.host(ap_config.get("ssid"), ap_config.get("password"))


_boot()
