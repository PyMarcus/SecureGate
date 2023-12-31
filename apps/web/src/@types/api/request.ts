import { Role } from '../schemas/session-user'

export interface SignInRequest {
  email: string
  password: string
}

export interface SignUpRequest {
  name: string
  email: string
  password: string
  role: Role
}

export interface CreateUserRequest {
  name: string
  email: string
  rfid: string
  authorized: boolean
  device_id: string
}

export interface CreateAdminRequest {
  name: string
  email: string
  password: string
  role: 'ADMIN'
}

export interface CreateDeviceRequest {
  id: string
  name: string
  wifi_ssid: string
  wifi_password: string
  version: string
}

export interface GetDeviceUsersRequest {
  deviceId: string
}

export interface GetDeviceHistoryRequest {
  deviceId: string
  date: string
}

export interface GetUserAccessHistoryRequest {
  userId: string
}

export interface DeviceActivationRequest {
  deviceId: string
  action: 'ACTIVATE' | 'DEACTIVATE'
}

export interface UpdateUserAuthorizationRequest {
  userId: string
  authorized: boolean
}

interface WifiConfig {
  ssid: string
  password: string
}

interface MqttConfig {
  host: string
  port: number
  user: string
  password: string
}

export interface ConfigureDeviceRequest {
  id: string
  mqtt: MqttConfig
  wifi: WifiConfig
}

export interface GetAdminsRequest {
  rootId: string
}
