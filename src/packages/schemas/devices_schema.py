from pydantic import BaseModel


class DeviceSchema(BaseModel):
    id: str
    name: str
    wifi_ssid: str
    wifi_password: str
    version: str


class DeviceActivationSchema(BaseModel):
    device_id: str
    action: str


class RFIDAuthenticationSchema(BaseModel):
    device_id: str
    rfid: str
