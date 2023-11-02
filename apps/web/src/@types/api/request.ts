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
}

export interface CreateDeviceRequest {
  name: string
  wifi_ssid: string
  wifi_password: string
  version: string
}

export interface GetDeviceHistoryRequest {
  deviceId: string
  startDate?: string
  endDate?: string
}

export interface GetUserAccessHistoryRequest {
  userId: string
}
