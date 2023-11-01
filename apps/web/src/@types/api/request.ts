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
  added_by: string
}
