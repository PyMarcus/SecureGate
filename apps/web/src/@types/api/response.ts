import { Role } from '@/@types/schemas/session-user'
import { AccessHistory } from '../schemas/access-history'
import { Device } from '../schemas/device'
import { User } from '../schemas/user'

export interface ApiError {
  success: false
  status_code: string
  message: string
}

export interface ApiResponse<T> {
  success: true
  status_code: string
  message: string
  data: T
}

// Session =====================================================================
interface SignInResponseData {
  user_id: string
  name: string
  email: string
  role: Role
  token: string
}
export type SignInResponse = ApiResponse<SignInResponseData>

type SignUpResponseData = true
export type SignUpResponse = ApiResponse<SignUpResponseData>

// Users =====================================================================

type CreateUserResponseData = true
export type CreateUserResponse = ApiResponse<CreateUserResponseData>

type UpdateUserAuthorizationResponseData = true
export type UpdateUserAuthorizationResponse =
  ApiResponse<UpdateUserAuthorizationResponseData>

// Devices =====================================================================
type GetAllDevicesResponseData = Device[]
export type GetAllDevicesResponse = ApiResponse<GetAllDevicesResponseData>

type CreateDeviceResponseData = true
export type CreateDeviceResponse = ApiResponse<CreateDeviceResponseData>

type GetDeviceUsers = User[]
export type GetDeviceUsersResponse = ApiResponse<GetDeviceUsers>

// Access History ==============================================================
type GetAccessHistoryResponseData = AccessHistory[]
export type GetAccessHistoryResponse = ApiResponse<GetAccessHistoryResponseData>
