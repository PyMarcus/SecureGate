import { Member } from '@/@types/schemas/member'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { cn } from '@/lib/utils'
import { ClockCounterClockwise, DotsThreeVertical } from '@phosphor-icons/react'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { TableCell, TableRow } from './ui/table'

interface MemberCardProps {
  member: Member
  isSelected: boolean
  onSelectRow: (member: Member) => void
}

export const MemberRow = ({
  member,
  isSelected,
  onSelectRow,
}: MemberCardProps) => {
  const displayId = member.id.split('-')[0]

  const handleSelectRow = () => onSelectRow(member)

  return (
    <TableRow className={cn(isSelected && 'bg-muted')}>
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
            <DropdownMenuLabel>Options for {member.name}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleSelectRow}>
              View History
              <DropdownMenuShortcut>
                <ClockCounterClockwise />
              </DropdownMenuShortcut>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
    </TableRow>
  )
}
