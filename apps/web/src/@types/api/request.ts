import { Role } from '../schemas/user'

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
