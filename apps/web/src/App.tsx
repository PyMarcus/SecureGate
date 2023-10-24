import { Toaster } from '@/components/ui/toaster'
import { queryClient } from '@/lib/react-query/client'
import { AppRoutes } from '@/routes/app-routes'
import { usePreferencesStore } from '@/stores/preferences-store'
import '@/styles/globals.css'
import { IconContext } from '@phosphor-icons/react'
import { useEffect } from 'react'
import { QueryClientProvider } from 'react-query'

export const App = () => {
  const { theme } = usePreferencesStore()

  useEffect(() => {
    const rootClassList = window.document.documentElement.classList
    theme === 'dark' ? rootClassList.add('dark') : rootClassList.remove('dark')
  }, [theme])

  return (
    <IconContext.Provider
      value={{
        size: 18,
      }}
    >
      <QueryClientProvider client={queryClient}>
        <AppRoutes />
        <Toaster duration={2000} />
      </QueryClientProvider>
    </IconContext.Provider>
  )
}
