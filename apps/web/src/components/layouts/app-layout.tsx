import { AppHeader } from '@/components/app-header'
import { Outlet } from 'react-router-dom'

export const AppLayout = () => {
  return (
    <div className="flex-1 flex flex-col relative">
      <AppHeader />

      <div className="flex flex-1 p-6 md:p-8">
        <Outlet />
      </div>
    </div>
  )
}
