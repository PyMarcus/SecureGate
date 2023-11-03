import { AccessHistory } from '@/@types/schemas/access-history'
import { TableCell, TableRow } from './ui/table'

interface AccessHistoryRowProps {
  history: AccessHistory
}

export const AccessHistoryRow = ({ history }: AccessHistoryRowProps) => {
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
