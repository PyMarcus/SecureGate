import { User } from '@/@types//schemas/user'
import { Role } from '@/@types/schemas/session-user'
import { AccessHistory } from '../schemas/access-history'
import { Device } from '../schemas/device'

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

// Members =====================================================================
type GetAllUsersResponseData = User[]
export type GetAllMembersResponse = ApiResponse<GetAllUsersResponseData>

type CreateUserResponseData = true
export type CreateUserResponse = ApiResponse<CreateUserResponseData>

// Devices =====================================================================
type GetAllDevicesResponseData = Device[]
export type GetAllDevicesResponse = ApiResponse<GetAllDevicesResponseData>

type CreateDeviceResponseData = true
export type CreateDeviceResponse = ApiResponse<CreateDeviceResponseData>

// Access History ==============================================================
type GetAccessHistoryResponseData = AccessHistory[]
export type GetAccessHistoryResponse = ApiResponse<GetAccessHistoryResponseData>
