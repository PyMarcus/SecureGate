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
  token: string
}

export interface SignUpRequest {
  email: string
  password: string
  name: string
}
