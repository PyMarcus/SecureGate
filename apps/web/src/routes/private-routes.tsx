import { Navigate, Outlet } from 'react-router-dom'

export const PrivateRoutes = () => {
  const authenticated = true
  return authenticated ? <Outlet /> : <Navigate to="/session" />
}
