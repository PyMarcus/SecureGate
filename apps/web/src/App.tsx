import { Toaster } from '@/components/ui/toaster'
import { AppRoutes } from '@/routes/app-routes'
import '@/styles/globals.css'
import { useEffect } from 'react'
import { usePreferencesStore } from './stores/preferences-store'

export const App = () => {
  const { theme } = usePreferencesStore()

  useEffect(() => {
    const rootClassList = window.document.documentElement.classList
    theme === 'dark' ? rootClassList.add('dark') : rootClassList.remove('dark')
  }, [theme])

  return (
    <>
      <AppRoutes />
      <Toaster duration={2000} />
    </>
  )
}
