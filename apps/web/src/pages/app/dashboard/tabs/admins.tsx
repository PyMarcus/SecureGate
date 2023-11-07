import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { useUserAdmins } from '@/services/api/requests/admins'
import { useAdminStore } from '@/stores/admin-store'
import { useSessionStore } from '@/stores/session-store'
import { Users } from '@phosphor-icons/react'
import { useEffect } from 'react'

export const Admins = () => {
  const { session } = useSessionStore()
  const { isLoadingAdmins, setIsLoadingAdmins } = useAdminStore()

  const { isLoading: deviceUsersLoading } = useUserAdmins({
    rootId: session?.user?.id || '-',
  })

  console.log(deviceUsersLoading)
  useEffect(() => {
    setIsLoadingAdmins(isLoadingAdmins)
  }, [isLoadingAdmins, setIsLoadingAdmins])

  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8">
      <ScrollArea className="w-full">
        <div className="w-[calc(100vw-3rem)] flex gap-6 md:gap-8 items-stretch">
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total de administradores
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <span>5</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Total de administradores cadastrados
              </p>
            </CardContent>
          </Card>
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>

      <Card className="flex-1 ">
        <CardHeader>
          <CardTitle>Administradores</CardTitle>
        </CardHeader>
        <CardContent></CardContent>
      </Card>
    </section>
  )
}
