import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { ScrollArea, ScrollBar } from './ui/scroll-area'

import { User } from '@/@types/schemas/user'
import { TableCell } from './ui/table'

const users: User[] = [
  {
    id: '8a9180aa-7684-11ee-b962-0242ac120002',
    name: 'John Doe 1',
    email: 'john1@doe.com',
    addedBy: 'a5669e1a-7684-11ee-b962-0242ac120002',
    authorized: true,
    rfId: '1234567890',
  },
  {
    id: '8da554ec-7684-11ee-b962-0242ac120002',
    name: 'John Doe 2',
    email: 'john2@doe.com',
    addedBy: 'a5669e1a-7684-11ee-b962-0242ac120002',
    authorized: false,
    rfId: '0987654321',
  },
  {
    id: '91dcb5aa-7684-11ee-b962-0242ac120002',
    name: 'John Doe 3',
    email: 'john3@doe.com',
    addedBy: 'a5669e1a-7684-11ee-b962-0242ac120002',
    authorized: true,
    rfId: '1234098765',
  },
  {
    id: '95e6f9f4-7684-11ee-b962-0242ac120002',
    name: 'John Doe 4',
    email: 'john4@doe.com',
    addedBy: 'a5669e1a-7684-11ee-b962-0242ac120002',
    authorized: false,
    rfId: '0987564321',
  },
  {
    id: '9a7c3c7a-7684-11ee-b362-0242ac120002',
    name: 'John Doe 5',
    email: 'john5@doe.com',
    addedBy: 'a5669e1a-7684-11ee-b962-0242ac120002',
    authorized: true,
    rfId: '1234567890',
  },
  {
    id: '9a7c3c7a-7684-11ee-b9562-0242ac120002',
    name: 'John Doe 6',
    email: 'john6@doe.com',
    addedBy: 'a5669e1a-7684-11ee-b962-0242ac120002',
    authorized: true,
    rfId: '1234567890',
  },
]

const UserHistoryRow = () => {
  return (
    <TableRow>
      <TableCell></TableCell>
      <TableCell></TableCell>
      <TableCell></TableCell>
      <TableCell></TableCell>
      <TableCell></TableCell>
    </TableRow>
  )
}

export const UserHistoryTable = () => {
  const hasFilteredMembers = users.length > 0

  return (
    <ScrollArea
      className="max-w-[calc(100vw-6rem)] md:max-w-[calc(100vw-8rem)]
      md:h-[calc(100vh-42rem)]"
    >
      {hasFilteredMembers ? (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead className="min-w-[100px]">Nome</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Autorizado</TableHead>
              <TableHead className="sr-only">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((user) => (
              <UserHistoryRow key={user.id} />
            ))}
          </TableBody>
        </Table>
      ) : (
        <div className="h-32 grid place-items-center">
          <p className="text-sm text-muted-foreground">
            Nenhum membro encontrado!
          </p>
        </div>
      )}
      <ScrollBar orientation="horizontal" />
      <ScrollBar orientation="vertical" />
    </ScrollArea>
  )
}
