import { AppHeader } from '@/components/app-header'
import { Outlet } from 'react-router-dom'
import { AppNavigation } from '../app-navigation'

export const AppLayout = () => {
  return (
    <div className="h-full w-full flex-1 flex flex-col relative">
      <AppHeader />

      <div className="flex flex-1 p-6 md:p-8 overflow-y-hidden overflow-x-hidden">
        <Outlet />
      </div>

      <div className="w-full md:hidden  bg-background">
        <AppNavigation mobile />
      </div>
    </div>
  )
}
