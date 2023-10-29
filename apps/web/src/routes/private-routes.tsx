import { Role } from '@/@types/schemas/user'
import { api } from '@/services/api/instance'
import { useSessionStore } from '@/stores/session-store'
import { Navigate, Outlet } from 'react-router-dom'

interface PrivateRoutesProps {
  enabledRole?: Role | null
}

export const PrivateRoutes = ({ enabledRole = null }: PrivateRoutesProps) => {
  const { session } = useSessionStore()

  if (session) {
    const { token, user } = session
    api.defaults.headers.Authorization = `Bearer ${token}`
    api.defaults.headers.userEmail = user.email

    if (enabledRole !== null) {
      return user.role === enabledRole ? <Outlet /> : <Navigate to="/404" />
    }
    return <Outlet />
  }
  return <Navigate to="/session/sign-in" />
}
