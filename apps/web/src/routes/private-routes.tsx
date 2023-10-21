import { Navigate, Outlet } from 'react-router-dom'

export const PrivateRoutes = () => {
  const authenticated = false
  return authenticated ? <Outlet /> : <Navigate to="/session/sign-in" />
}
