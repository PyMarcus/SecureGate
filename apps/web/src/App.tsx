import { Toaster } from '@/components/ui/toaster'
import { queryClient } from '@/lib/react-query/client'
import { AppRoutes } from '@/routes/app-routes'
import { usePreferencesStore } from '@/stores/preferences-store'
import '@/styles/globals.css'
import { useEffect } from 'react'
import { QueryClientProvider } from 'react-query'

export const App = () => {
  const { theme } = usePreferencesStore()

  useEffect(() => {
    const rootClassList = window.document.documentElement.classList
    theme === 'dark' ? rootClassList.add('dark') : rootClassList.remove('dark')
  }, [theme])

  return (
    <QueryClientProvider client={queryClient}>
      <AppRoutes />
      <Toaster duration={2000} />
    </QueryClientProvider>
  )
}
