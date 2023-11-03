import { AccessHistory } from '@/@types/schemas/access-history'
import { format } from 'date-fns'
import { TableCell, TableRow } from './ui/table'

interface AccessHistoryRowProps {
  history: AccessHistory
}

export const AccessHistoryRow = ({ history }: AccessHistoryRowProps) => {
  const displayId = history.id.split('-')[0]

  const displayDate = format(new Date(`${history.when}Z`), 'dd/MM/yyyy HH:mm')

  return (
    <TableRow>
      <TableCell>{displayId}</TableCell>
      <TableCell>{history.user_name}</TableCell>
      <TableCell>{history.device_name}</TableCell>
      <TableCell>{displayDate}</TableCell>
    </TableRow>
  )
}
