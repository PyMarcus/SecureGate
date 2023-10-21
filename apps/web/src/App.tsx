import { Toaster } from '@/components/ui/toaster'
import { AppRoutes } from '@/routes/app-routes'
import '@/styles/globals.css'

export const App = () => {
  return (
    <>
      <AppRoutes />
      <Toaster duration={2000} />
    </>
  )
}
