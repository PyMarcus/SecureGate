import { User } from '@/@types/schemas/user'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { cn } from '@/lib/utils'
import {
  ClockCounterClockwise,
  DotsThreeVertical,
  LockKey,
  LockKeyOpen,
  X,
} from '@phosphor-icons/react'
import { useState } from 'react'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { TableCell, TableRow } from './ui/table'

interface UserCardProps {
  user: User
  isSelected: boolean
  onSelectRow: (user: User) => void
}

type Authorization = 'Sim' | 'Não'

export const UserRow = ({ user, isSelected, onSelectRow }: UserCardProps) => {
  const [authorization, setAuthorization] = useState<Authorization>(
    user.authorized ? 'Sim' : 'Não',
  )

  const isAuthorized = authorization === 'Sim'

  const displayId = user.id.split('-')[0]

  const handleSelectRow = () => onSelectRow(user)
  const handleAuthorizationChange = (value: string) =>
    setAuthorization(value as Authorization)

  return (
    <TableRow className={cn(isSelected && 'bg-muted')}>
      <TableCell>{displayId}</TableCell>
      <TableCell>{user.name}</TableCell>
      <TableCell>{user.email}</TableCell>
      <TableCell>
        <Badge variant={isAuthorized ? 'default' : 'destructive'}>
          {authorization}
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
            <DropdownMenuLabel>Opções para {user.name}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleSelectRow}>
              {isSelected ? 'Close History' : 'View History'}
              <DropdownMenuShortcut>
                {isSelected ? <X /> : <ClockCounterClockwise />}
              </DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuSub>
              <DropdownMenuSubTrigger className="cursor-pointer">
                Autorizado
              </DropdownMenuSubTrigger>
              <DropdownMenuPortal>
                <DropdownMenuSubContent>
                  <DropdownMenuRadioGroup
                    value={authorization}
                    onValueChange={handleAuthorizationChange}
                  >
                    <DropdownMenuRadioItem
                      value="Sim"
                      className="cursor-pointer"
                    >
                      Sim
                      <DropdownMenuShortcut>
                        <LockKeyOpen size={22} className="text-emerald-500" />
                      </DropdownMenuShortcut>
                    </DropdownMenuRadioItem>
                    <DropdownMenuRadioItem
                      value="Não"
                      className="cursor-pointer"
                    >
                      Não
                      <DropdownMenuShortcut>
                        <LockKey size={22} className="text-destructive" />
                      </DropdownMenuShortcut>
                    </DropdownMenuRadioItem>
                  </DropdownMenuRadioGroup>
                </DropdownMenuSubContent>
              </DropdownMenuPortal>
            </DropdownMenuSub>
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
    </TableRow>
  )
}
