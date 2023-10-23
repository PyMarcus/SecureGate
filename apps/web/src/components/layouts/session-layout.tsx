import { LockKey } from '@phosphor-icons/react'
import { Outlet } from 'react-router-dom'

export const SessionLayout = () => {
  return (
    <div
      className="min-h-screen w-screen max-w-[100vw] overflow-y-auto
    overflow-x-hidden bg-background grid grid-cols-1 grid-rows-6 md:grid-cols-2
    md:grid-rows-1"
    >
      <div className="md:bg-zinc-900 p-6 md:p-8 flex flex-col justify-between">
        <strong
          className="inline-flex items-center gap-1 text-foreground
        md:text-neutral-50 py-1"
        >
          <span>
            <LockKey weight="bold" className="text-2xl" />
          </span>
          <span className="text-lg font-medium">SecureGate</span>
        </strong>
        <p className="hidden md:block text-foreground md:text-neutral-50">
          Secure Gate is a complete access management solution, combining a
          user-friendly web app, a robust backend system, and ESP32 integration.
          It enables users to manage gate access by RFID cards, providing better
          security and convenience.
        </p>
      </div>

      <div className="row-span-5 p-6 md:p-8 grid place-items-center relative">
        <Outlet />
      </div>
    </div>
  )
}
