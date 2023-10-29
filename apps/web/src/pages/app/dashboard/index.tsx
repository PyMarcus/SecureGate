import { ConfirmDialog } from '@/components/confirm-dialog'
import { GatesSelector } from '@/components/gates-selector'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useSessionStore } from '@/stores/session-store'
import { LockKeyOpen, PlusCircle } from '@phosphor-icons/react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'

export const Dashboard = () => {
  const { session } = useSessionStore()

  const navigate = useNavigate()
  const { pathname } = useLocation()
  const { role } = session!.user

  const currentTab = pathname.split('/')[2]
  const isRoot = role === 'ROOT'

  const handleTabsNavigation = (value: string) => {
    navigate(`/dashboard/${value}`)
  }

  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8 bg-background">
      <header className="flex items-center justify-between flex-col md:flex-row gap-4">
        <h2 className="text-3xl font-bold tracking-tight self-start">
          Dashboard
        </h2>
        <div className="inline-flex gap-4 justify-end w-full">
          <GatesSelector />

          {isRoot && (
            <Button className="space-x-2 min-w-max">
              <PlusCircle />
              <span className="sr-only md:not-sr-only">New gate</span>
            </Button>
          )}

          <ConfirmDialog
            title="Are you sure you want to open this gate?"
            description="This action cannot be undone. After opening the gate, you won't be able to close it automatically."
            trigger={
              <Button variant="destructive" className="space-x-2 min-w-max">
                <LockKeyOpen />
                <span className="sr-only md:not-sr-only">Open gate</span>
              </Button>
            }
          />
        </div>
      </header>

      <Tabs
        defaultValue="overview"
        value={currentTab}
        className="flex flex-1 flex-col gap-6 md:gap-8"
        onValueChange={handleTabsNavigation}
      >
        <TabsList
          className="w-full sm:w-auto justify-start flex-wrap h-auto 
        self-start"
        >
          <TabsTrigger value="overview" className="flex-1">
            Overview
          </TabsTrigger>

          {isRoot && (
            <TabsTrigger value="users" className="flex-1">
              Users
            </TabsTrigger>
          )}

          <TabsTrigger value="members" className="flex-1">
            Members
          </TabsTrigger>
          <TabsTrigger value="analytics" className="flex-1">
            Analytics
          </TabsTrigger>
        </TabsList>

        <TabsContent
          value={currentTab}
          className="flex-1 flex flex-col gap-6 md:gap-8 justify-between"
        >
          <Outlet />
        </TabsContent>
      </Tabs>
    </section>
  )
}
