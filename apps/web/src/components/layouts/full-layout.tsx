import { Outlet } from 'react-router-dom'

export const FullLayout = () => {
  return (
    <div
      className="flex min-h-screen w-screen max-w-[100vw] flex-col
    overflow-y-auto overflow-x-hidden bg-background"
    >
      <Outlet />
    </div>
  )
}
