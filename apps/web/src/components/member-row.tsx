import { Member } from '@/@types/schemas/member'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { DotsThreeVertical } from '@phosphor-icons/react'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { TableCell, TableRow } from './ui/table'

interface MemberCardProps {
  member: Member
}

export const MemberRow = ({ member }: MemberCardProps) => {
  const displayId = member.id.split('-')[0]

  return (
    <TableRow>
      <TableCell>{displayId}</TableCell>
      <TableCell>{member.name}</TableCell>
      <TableCell>{member.email}</TableCell>
      <TableCell>
        <Badge variant={member.authorized ? 'default' : 'destructive'}>
          {member.authorized ? 'Yes' : 'No'}
        </Badge>
      </TableCell>
      <TableCell>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <DotsThreeVertical />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Profile</DropdownMenuItem>
            <DropdownMenuItem>Billing</DropdownMenuItem>
            <DropdownMenuItem>Team</DropdownMenuItem>
            <DropdownMenuItem>Subscription</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
    </TableRow>
  )
}
