import { Role } from '@/@types/schemas/user'

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
