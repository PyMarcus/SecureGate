from pydantic import BaseModel


class DeviceSchema(BaseModel):
    name: str
    wifi_ssid: str
    wifi_password: str
    version: str
