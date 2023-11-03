import { User } from '@/@types/schemas/user'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { UserRow } from '@/components/user-row'

import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { useState } from 'react'
import { LoadingIndicator } from './loading-indicator'
import { NewUserDialog } from './new-user-dialog'

interface UsersTableProps {
  isLoading: boolean
  users: User[]
  selectedUser: User | null
  onSelectUser: (member: User) => void
}

export const UsersTable = ({
  isLoading,
  users,
  selectedUser,
  onSelectUser,
}: UsersTableProps) => {
  const [filter, setFilter] = useState('')

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setFilter(e.target.value)

  const filteredUsers = users.filter(({ name }) =>
    name.toLowerCase().includes(filter.toLowerCase()),
  )
  const hasFilteredUsers = filteredUsers.length > 0

  return (
    <div className="flex flex-col gap-4">
      <div
        className="flex justify-between items-center sticky
      inset-x-px md:max-w-none gap-4"
      >
        <Input
          placeholder="Buscar usuário"
          className="m-px max-w-[16rem]"
          onChange={handleFilterChange}
        />
        <NewUserDialog />
      </div>
      <ScrollArea
        className="max-w-[calc(100vw-6rem)] md:max-w-[calc(100vw-8rem)]
      md:h-[calc(100vh-42rem)]"
      >
        {hasFilteredUsers ? (
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
              {filteredUsers.map((user) => {
                const rowIsSelected = user.id === selectedUser?.id
                return (
                  <UserRow
                    key={user.id}
                    user={user}
                    isSelected={rowIsSelected}
                    onSelectRow={onSelectUser}
                  />
                )
              })}
            </TableBody>
          </Table>
        ) : (
          <div className="h-32 grid place-items-center">
            {isLoading ? (
              <LoadingIndicator />
            ) : (
              <p className="text-sm text-muted-foreground">
                Nenhum usuário encontrado!
              </p>
            )}
          </div>
        )}

        <ScrollBar orientation="horizontal" />
        <ScrollBar orientation="vertical" />
      </ScrollArea>
    </div>
  )
}
