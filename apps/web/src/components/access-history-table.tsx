import { AccessHistory } from '@/@types/schemas/access-history'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { AccessHistoryRow } from './access-history-row'
import { LoadingIndicator } from './loading-indicator'

interface AccessHistoryTableProps {
  isLoading: boolean
  accessHistory: AccessHistory[]
}

export const AccessHistoryTable = ({
  isLoading,
  accessHistory,
}: AccessHistoryTableProps) => {
  const hasAccessHistory = accessHistory.length > 0

  return (
    <ScrollArea
      className="max-w-[calc(100vw-6rem)] md:max-w-[calc(100vw-8rem)]
    md:h-[calc(100vh-42rem)]"
    >
      {hasAccessHistory ? (
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
            {accessHistory.map((history) => (
              <AccessHistoryRow key={history.id} history={history} />
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
