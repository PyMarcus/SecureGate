from apps.emulator.src.utils.log import Log


class WifiService:
    def __init__(self):
        ...

    def host(self, ssid: str, password: str):
        """
        Create a WiFi hotspot.
        """
        Log.info(f"Hosting WiFi network ssid: {ssid} with password: {password}")

    def connect(self, ssid: str, password: str):
        """
        Connect to a WiFi network.
        """
        Log.info(f"Connecting to WiFi network ssid: {ssid}")
