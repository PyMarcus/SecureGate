import { useSessionStore } from '@/stores/session-store'
import { Navigate, Outlet } from 'react-router-dom'

export const PrivateRoutes = () => {
  const { session } = useSessionStore()
  return session ? <Outlet /> : <Navigate to="/session/sign-in" />
}
