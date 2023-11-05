import { ConfirmDialog } from '@/components/confirm-dialog'
import { GatesSelector } from '@/components/gates-selector'
import { LoadingIndicator } from '@/components/loading-indicator'
import { NewGateDialog } from '@/components/new-gate-dialog'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useToast } from '@/components/ui/use-toast'
import { useDeviceActivation } from '@/services/api/requests/devices'
import { useDeviceStore } from '@/stores/device-store'
import { useSessionStore } from '@/stores/session-store'
import { LockKeyOpen } from '@phosphor-icons/react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'

export const Dashboard = () => {
  const { session } = useSessionStore()
  const { currentDevice } = useDeviceStore()

  const { toast } = useToast()

  const navigate = useNavigate()
  const { pathname } = useLocation()
  const { role } = session!.user

  const currentTab = pathname.split('/')[2]
  const isRoot = role === 'ROOT'

  const handleTabsNavigation = (value: string) => {
    navigate(`/painel/${value}`)
  }

  const { isLoading: isActivating, mutateAsync: activateDevice } =
    useDeviceActivation()

  const handleActivateDevice = async () => {
    if (currentDevice) {
      const response = await activateDevice({
        deviceId: currentDevice.id,
        action: 'ACTIVATE',
      })
      if (response && response.success) {
        const { data } = response

        toast({
          title: 'Portão ativado com sucesso!',
          description: `Agora você pode abrir o portão "${data.name}"`,
        })
      }
    }
  }

  return (
    <section className="flex-1 flex">
      <Tabs
        defaultValue="overview"
        value={currentTab}
        className="flex-1 flex flex-col"
        onValueChange={handleTabsNavigation}
      >
        <header
          className="flex flex-col sticky -top-6 md:-top-8 bg-background 
        z-30 gap-6 md:gap-8 py-6 md:py-8"
        >
          <div className="flex items-center justify-between flex-col md:flex-row gap-4">
            <h2 className="text-3xl font-bold tracking-tight self-start">
              Painel
            </h2>
            <div className="inline-flex gap-4 justify-end w-full">
              <GatesSelector />

              {isRoot && <NewGateDialog />}

              <ConfirmDialog
                title="Are you sure you want to open this gate?"
                description="This action cannot be undone. After opening the gate, you won't be able to close it automatically."
                onConfirm={handleActivateDevice}
                trigger={
                  <Button
                    variant="destructive"
                    className="space-x-2 min-w-max"
                    disabled={!currentDevice || isActivating}
                  >
                    {isActivating ? <LoadingIndicator /> : <LockKeyOpen />}
                    <span className="sr-only md:not-sr-only">Abrir portão</span>
                  </Button>
                }
              />
            </div>
          </div>
          <TabsList
            className="w-full sm:w-auto justify-start flex-wrap h-auto 
        self-start"
          >
            <TabsTrigger value="geral" className="flex-1">
              Geral
            </TabsTrigger>
            <TabsTrigger value="usuarios" className="flex-1">
              Usuários
            </TabsTrigger>
            <TabsTrigger value="graficos" className="flex-1" disabled>
              Gráficos
            </TabsTrigger>
            {isRoot && (
              <TabsTrigger value="admins" className="flex-1">
                Administradores
              </TabsTrigger>
            )}
          </TabsList>
        </header>

        <ScrollArea className="flex-1">
          <TabsContent
            value={currentTab}
            className="mt-0 flex-1 flex flex-col gap-6 md:gap-8 justify-between 
            h-[calc(100vh-23rem)] md:h-[calc(100vh-21rem)]"
          >
            <Outlet />
          </TabsContent>
        </ScrollArea>
      </Tabs>
    </section>
  )
}
