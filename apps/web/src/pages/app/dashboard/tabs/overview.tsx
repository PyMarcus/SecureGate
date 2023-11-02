import { LoadingIndicator } from '@/components/loading-indicator'
import { OverviewChart } from '@/components/overview-chart'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getDeviceAccessHistoryRequest } from '@/services/api/requests/devices'
import { useDeviceStore } from '@/stores/device-store'
import { useUserStore } from '@/stores/user-store'
import { LockKeyOpen, Users } from '@phosphor-icons/react'
import { format, sub } from 'date-fns'
import { useEffect } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'

export const Overview = () => {
  const {
    isLoadingDevices,
    deviceAccessHistory,
    currentDevice,
    setDeviceAccessHistory,
  } = useDeviceStore()
  const { users, isLoadingUsers } = useUserStore()
  const totalUsers = users.length

  const currentDate = new Date()
  const twentyFourHoursAgo = sub(currentDate, { hours: 24 })

  const getDeviceAccessHistory = () =>
    getDeviceAccessHistoryRequest({
      deviceId: currentDevice!.id,
      startDate: format(twentyFourHoursAgo, 'yyyy-MM-dd HH:mm'),
      endDate: format(twentyFourHoursAgo, 'yyyy-MM-dd HH:mm'),
    })

  const {
    isLoading: isLoadingDeviceAccessHistory,
    data: deviceAccessHistoryResponse,
  } = useQuery('deviceAccessHistory', getDeviceAccessHistory, {
    enabled: !!currentDevice,
  })

  useEffect(() => {
    if (deviceAccessHistoryResponse && deviceAccessHistoryResponse.success) {
      console.log(deviceAccessHistoryResponse.data)
      setDeviceAccessHistory(deviceAccessHistoryResponse.data || [])
    }
  }, [deviceAccessHistoryResponse, setDeviceAccessHistory])

  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8">
      <ScrollArea className="w-full">
        <div className="w-[calc(100vw-3rem)] flex gap-6 md:gap-8 items-stretch">
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total de usuários
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {isLoadingUsers ? (
                  <LoadingIndicator />
                ) : (
                  <span>{totalUsers}</span>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Total de usuários cadastrados
              </p>
            </CardContent>
          </Card>
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total de acessos
              </CardTitle>
              <LockKeyOpen className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {isLoadingDevices ? (
                  <LoadingIndicator />
                ) : (
                  <span>{deviceAccessHistory.length}</span>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Total de acessos hoje
              </p>
            </CardContent>
          </Card>
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>

      <div
        className="grid flex-1 grid-rows-2 md:grid-rows-1 md:grid-cols-7 
      gap-6 md:gap-8"
      >
        <Card className="md:col-span-4">
          <CardHeader>
            <div className="inline-flex items-center justify-between">
              <CardTitle>Geral</CardTitle>
              <Button variant="link" size="sm" asChild>
                <Link to="/painel/graficos">Ver mais</Link>
              </Button>
            </div>
            <CardDescription className="mt-0">
              Acessos nas últimas 24 horas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ScrollArea
              className="max-w-[calc(100vw-6rem)] 
            md:max-w-[calc(100vw-8rem)]"
            >
              {isLoadingDeviceAccessHistory ? (
                <div className="h-[310px] grid place-items-center">
                  <LoadingIndicator />
                </div>
              ) : (
                <OverviewChart history={deviceAccessHistory} />
              )}

              <ScrollBar orientation="horizontal" />
            </ScrollArea>
          </CardContent>
        </Card>
        <Card className="md:col-span-3">
          <CardHeader>
            <div className="inline-flex items-center justify-between">
              <CardTitle>Últimos acessos</CardTitle>
              <Button variant="link" size="sm" asChild>
                <Link to="/painel/membros">Ver todos</Link>
              </Button>
            </div>
            <CardDescription className="mt-0">
              Últimos 10 acessos
            </CardDescription>
          </CardHeader>
          <CardContent></CardContent>
        </Card>
      </div>
    </section>
  )
}
