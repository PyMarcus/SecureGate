import { Outlet } from 'react-router-dom'

export const SessionLayout = () => {
  return (
    <div
      className="min-h-screen w-screen  overflow-y-auto overflow-x-hidden
      bg-background grid place-items-center"
    >
      <Outlet />
    </div>
  )
}
