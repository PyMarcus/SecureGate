import { Outlet } from 'react-router-dom'
import { DashboardHeader } from '../dashboard-header'

export const DashboardLayout = () => {
  return (
    <div className="flex-1 flex flex-col">
      <DashboardHeader />

      <div className="flex-1 p-6 md:p-8">
        <Outlet />
      </div>
    </div>
  )
}
