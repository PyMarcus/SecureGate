import { UserNav } from '@/components/user-nav'
import { useSessionStore } from '@/stores/session-store'

export const DashboardHeader = () => {
  const { session, clearSession } = useSessionStore()

  const { name, email } = session!.user

  return (
    <div className="w-full px-6 md:px-8 border-b">
      <header className="flex items-center justify-between h-16">
        <span>header</span>

        <div className="inline-flex gap-4 items-center">
          <div className="hidden md:flex flex-col space-y-1 text-end">
            <p className="text-sm font-medium leading-none">{name}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {email}
            </p>
          </div>
          <UserNav name={name} email={email} onSignOut={clearSession} />
        </div>
      </header>
    </div>
  )
}
