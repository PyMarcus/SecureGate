from src.packages.logger.Logger import Logger

logger = Logger('wifi_service')

class WifiService:
    def __init__(self):
        ...

    def host(self, ssid: str, password: str):
        """
        Create a WiFi hotspot.
        """
        logger.info(f"Hosting WiFi network ssid: {ssid} with password: {password}")

    def connect(self, ssid: str, password: str):
        """
        Connect to a WiFi network.
        """
        logger.info(f"Connecting to WiFi network ssid: {ssid}")
