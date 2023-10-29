import { Member } from '@/@types/schemas/member'
import { MemberRow } from '@/components/member-row'
import { useState } from 'react'
import { Input } from './ui/input'
import { Table, TableBody, TableHead, TableHeader, TableRow } from './ui/table'

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
]

export const MembersTable = () => {
  const [filter, setFilter] = useState('')

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setFilter(e.target.value)

  const filteredMembers = members.filter(({ name }) =>
    name.toLowerCase().includes(filter.toLowerCase()),
  )
  console.log(filteredMembers)

  return (
    <div className="flex flex-col gap-4">
      <Input
        placeholder="Search members"
        className="m-px max-w-[16rem]"
        onChange={handleFilterChange}
      />

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
          {members.map((member) => (
            <MemberRow key={member.id} member={member} />
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
