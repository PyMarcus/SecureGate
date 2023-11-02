import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { ScrollArea, ScrollBar } from './ui/scroll-area'

import { AccessHistory } from '@/@types/schemas/access-history'
import { getUserAccessHistoryRequest } from '@/services/api/requests/users'
import { useUserStore } from '@/stores/user-store'
import { useQuery } from 'react-query'
import { LoadingIndicator } from './loading-indicator'
import { TableCell } from './ui/table'

interface UserHistoryRowProps {
  history: AccessHistory
}

const UserHistoryRow = ({ history }: UserHistoryRowProps) => {
  const displayId = history.id.split('-')[0]
  return (
    <TableRow>
      <TableCell>{displayId}</TableCell>
      <TableCell>{history.user_name}</TableCell>
      <TableCell>{history.device_name}</TableCell>
      <TableCell>{history.when}</TableCell>
    </TableRow>
  )
}

export const UserHistoryTable = () => {
  const { selectedUser } = useUserStore()

  const getUserAccessHistory = () =>
    getUserAccessHistoryRequest({ userId: selectedUser!.id })

  const hasSelectedUser = !!selectedUser
  const { data: userAccessHistory, isLoading } = useQuery(
    ['userAccessHistory', selectedUser!.id],
    getUserAccessHistory,
    { enabled: hasSelectedUser },
  )

  const hasUserAccessHistory = userAccessHistory && userAccessHistory.data

  return (
    <ScrollArea
      className="max-w-[calc(100vw-6rem)] md:max-w-[calc(100vw-8rem)]
      md:h-[calc(100vh-42rem)]"
    >
      {hasUserAccessHistory ? (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead className="min-w-[100px]">Nome</TableHead>
              <TableHead>Portão</TableHead>
              <TableHead>Data</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {userAccessHistory.data.map((history) => (
              <UserHistoryRow key={history.id} history={history} />
            ))}
          </TableBody>
        </Table>
      ) : (
        <div className="h-32 grid place-items-center">
          {isLoading ? (
            <LoadingIndicator />
          ) : (
            <p className="text-sm text-muted-foreground">
              Nenhum histórico encontrado!
            </p>
          )}
        </div>
      )}
      <ScrollBar orientation="horizontal" />
      <ScrollBar orientation="vertical" />
    </ScrollArea>
  )
}
