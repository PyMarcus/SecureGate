import { Role } from '@/@types/schemas/user'

export interface ApiError {
  error: string
  status: string
}

export interface SignInResponse {
  error: null
  status: string
  message: string
  user_request: string
  email: string
  time: string
  user_id: string
  role: Role
  token: string
}

export interface SignUpRequest {
  email: string
  password: string
  name: string
  role: Role
}
