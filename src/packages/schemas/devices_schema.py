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


class DeviceMQTTConfigSchema(BaseModel):
    host: str
    port: int
    user: str
    password: str


class DeviceWiFiConfigSchema(BaseModel):
    ssid: str
    password: str


class DeviceConfigSchema(BaseModel):
    id: str
    mqtt: DeviceMQTTConfigSchema
    wifi: DeviceWiFiConfigSchema
