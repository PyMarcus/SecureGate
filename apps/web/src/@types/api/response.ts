import { User } from '@/@types//schemas/user'
import { Role } from '@/@types/schemas/session-user'

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
