import { Member } from '@/@types/schemas/member'
import { MemberRow } from '@/components/member-row'
import { NewMemberDialog } from '@/components/new-member-dialog'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useState } from 'react'
import { ScrollArea, ScrollBar } from './ui/scroll-area'

const members: Member[] = [
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

interface MembersTableProps {
  selectedMember: Member | null
  onSelectMember: (member: Member) => void
}

export const MembersTable = ({
  selectedMember,
  onSelectMember,
}: MembersTableProps) => {
  const [filter, setFilter] = useState('')

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setFilter(e.target.value)

  const filteredMembers = members.filter(({ name }) =>
    name.toLowerCase().includes(filter.toLowerCase()),
  )
  const hasFilteredMembers = filteredMembers.length > 0

  return (
    <div className="flex flex-col gap-4">
      <div
        className="flex justify-between items-center sticky
      inset-x-px md:max-w-none gap-4"
      >
        <Input
          placeholder="Search members"
          className="m-px max-w-[16rem]"
          onChange={handleFilterChange}
        />
        <NewMemberDialog />
      </div>
      <ScrollArea
        className="max-w-[calc(100vw-6rem)] md:max-w-[calc(100vw-8rem)]
      md:h-[calc(100vh-42rem)]"
      >
        {hasFilteredMembers ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead className="min-w-[100px]">Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Authorized</TableHead>
                <TableHead className="sr-only">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredMembers.map((member) => {
                const rowIsSelected = member.id === selectedMember?.id
                return (
                  <MemberRow
                    key={member.id}
                    member={member}
                    isSelected={rowIsSelected}
                    onSelectRow={onSelectMember}
                  />
                )
              })}
            </TableBody>
          </Table>
        ) : (
          <p className="text-sm text-muted-foreground">No members found</p>
        )}
        <ScrollBar orientation="horizontal" />
        <ScrollBar orientation="vertical" />
      </ScrollArea>
    </div>
  )
}
