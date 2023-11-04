from pydantic import BaseModel


class DeviceSchema(BaseModel):
    id: str
    name: str
    wifi_ssid: str
    wifi_password: str
    version: str
