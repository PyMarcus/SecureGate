import { Outlet } from 'react-router-dom'

export const FullLayout = () => {
  return (
    <div
      className="flex h-screen w-screen max-w-[100vw] flex-col overflow-hidden 
    bg-background"
    >
      <Outlet />
    </div>
  )
}
