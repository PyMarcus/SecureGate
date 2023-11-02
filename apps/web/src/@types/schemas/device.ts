export interface Device {
  id: string
  name: string
  version: string
  wifi_ssid: string
}

export interface DeviceWithPass extends Device {
  wifi_password: string
}
