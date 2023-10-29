import { UserNav } from '@/components/user-nav'
import { useSessionStore } from '@/stores/session-store'
import { LockKey } from '@phosphor-icons/react'
import { Link } from 'react-router-dom'
import { AppNavigation } from './app-navigation'

export const AppHeader = () => {
  const { session, clearSession } = useSessionStore()

  const { name, email } = session!.user

  return (
    <div className="w-full px-6 md:px-8 border-b sticky bg-background top-0 inset-x-0">
      <header className="flex items-center justify-between h-16 gap-12">
        <Link
          to="/dashboard"
          className="text-xl font-bold inline-flex gap-1 items-center leading-none"
        >
          <LockKey weight="bold" size={23} className="text-tertiary" />
          <div className="hidden md:block">SecureGate</div>
          <span className="md:hidden">SG</span>
        </Link>

        <div className="hidden md:block flex-1">
          <AppNavigation />
        </div>

        <div className="inline-flex gap-4 items-center">
          <div className="hidden md:flex flex-col space-y-1 text-end">
            <p className="text-sm font-medium leading-none">{name}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {email}
            </p>
          </div>
          <UserNav
            avatar="/user.svg"
            name={name}
            email={email}
            onSignOut={clearSession}
          />
        </div>
      </header>
    </div>
  )
}
