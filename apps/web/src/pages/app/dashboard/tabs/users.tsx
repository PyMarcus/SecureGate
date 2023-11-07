import { AccessHistory } from '@/@types/schemas/access-history'
import { User } from '@/@types/schemas/user'
import { AccessHistoryTable } from '@/components/access-history-table'
import { LoadingIndicator } from '@/components/loading-indicator'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { UsersTable } from '@/components/users-table'
import { useUserAccessHistory } from '@/services/api/requests/users'
import { useDeviceStore } from '@/stores/device-store'
import { useUserStore } from '@/stores/user-store'
import {
  IdentificationCard,
  LockKeyOpen,
  Users as UsersIcon,
} from '@phosphor-icons/react'
import { useEffect, useRef, useState } from 'react'

export const Users = () => {
  const [accessHistory, setAccessHistory] = useState<AccessHistory[]>([])

  const {
    users,
    selectedUser,
    isLoadingUsers,
    setSelectedUser,
    removeSelectedUser,
  } = useUserStore()
  const { isLoadingDevices, deviceAccessHistory } = useDeviceStore()

  const { isLoading: isLoadingUserAccessHistory, data: userAccessHistory } =
    useUserAccessHistory({
      userId: selectedUser?.id || '-',
    })

  useEffect(() => {
    if (userAccessHistory && userAccessHistory.success) {
      setAccessHistory(userAccessHistory.data)
    }
  }, [userAccessHistory])

  const memberHistoryRef = useRef<HTMLHeadingElement | null>(null)

  const handleSelectMember = (member: User) => {
    if (member.id === selectedUser?.id) {
      return removeSelectedUser()
    }

    setSelectedUser(member)
    if (memberHistoryRef.current) {
      memberHistoryRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }

  const totalUsers = users.length || 0
  const totalAuthorizedUsers =
    users.filter(({ authorized }) => authorized) || []

  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8 ">
      <ScrollArea className="w-full">
        <div className="w-[calc(100vw-3rem)] flex gap-6 md:gap-8 items-stretch">
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total de usuários
              </CardTitle>
              <UsersIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <span>
                  {isLoadingUsers ? (
                    <LoadingIndicator />
                  ) : (
                    <span>{totalUsers}</span>
                  )}
                </span>
              </div>
              <p className="text-xs text-muted-foreground">
                Total de usuários cadastrados
              </p>
            </CardContent>
          </Card>

          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Usuários autorizados
              </CardTitle>
              <IdentificationCard className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {isLoadingUsers ? (
                  <LoadingIndicator />
                ) : (
                  <div>
                    <span>{totalAuthorizedUsers.length}</span>
                    <span className="text-sm font-medium">/{totalUsers}</span>
                  </div>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Total de usuários autorizados a entrar
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
                  <div>
                    <span>{deviceAccessHistory.length}</span>
                  </div>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Total de acessos realizados hoje
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
            <CardTitle>Usuários</CardTitle>
            <CardDescription className="mt-0">
              Usuários cadastrados
            </CardDescription>
          </CardHeader>
          <CardContent>
            <UsersTable
              isLoading={isLoadingUsers}
              users={users}
              selectedUser={selectedUser}
              onSelectUser={handleSelectMember}
            />
          </CardContent>
        </Card>
        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle ref={memberHistoryRef}>Histórico de acesso</CardTitle>
            <CardDescription className="mt-0">
              Histórico de acesso do usuário selecionado
            </CardDescription>
          </CardHeader>
          <CardContent>
            {selectedUser ? (
              <AccessHistoryTable
                isLoading={isLoadingUserAccessHistory}
                accessHistory={accessHistory}
              />
            ) : (
              <div className="h-32 grid place-items-center">
                <p className="text-sm text-muted-foreground">
                  Nenhum usuário selecionado!
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
