export type Role = 'ROOT' | 'ADMIN'

export interface SessionUser {
  id: string
  name: string
  email: string
  role: Role
}
