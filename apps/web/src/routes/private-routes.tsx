import { api } from '@/services/api/instance'
import { useSessionStore } from '@/stores/session-store'
import { Navigate, Outlet } from 'react-router-dom'

export const PrivateRoutes = () => {
  const { session } = useSessionStore()

  if (session) {
    api.defaults.headers.Authorization = `Bearer ${session.token}`
    return <Outlet />
  }
  return <Navigate to="/session/sign-in" />
}
