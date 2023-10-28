export type Role = 'ROOT' | 'ADMIN'

export interface User {
  id: string
  name: string
  email: string
  role: Role
}
