import { User } from '@/@types/schemas/user'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
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
import { TableCell, TableRow } from '@/components/ui/table'
import { cn } from '@/lib/utils'
import { useUpdateUserAuthorization } from '@/services/api/requests/users'
import {
  ClockCounterClockwise,
  DotsThreeVertical,
  LockKey,
  LockKeyOpen,
  X,
} from '@phosphor-icons/react'
import { toast } from './ui/use-toast'

interface UserCardProps {
  user: User
  isSelected: boolean
  onSelectRow: (user: User) => void
}

export const UserRow = ({ user, isSelected, onSelectRow }: UserCardProps) => {
  const displayId = user.id.split('-')[0]

  const handleSelectRow = () => onSelectRow(user)

  const { mutateAsync } = useUpdateUserAuthorization()

  const handleAuthorizationChange = async (value: string) => {
    const response = await mutateAsync({
      userId: user.id,
      authorized: value === 'Sim',
    })
    if (response && response.success) {
      toast({
        title: 'Usuário atualizado!',
        description: 'Permissão de acesso atualizada com sucesso.',
      })
    }
  }

  return (
    <TableRow className={cn(isSelected && 'bg-muted')}>
      <TableCell>{displayId}</TableCell>
      <TableCell>{user.name}</TableCell>
      <TableCell>{user.email}</TableCell>
      <TableCell>
        <Badge variant={user.authorized ? 'success' : 'destructive'}>
          {user.authorized ? 'Sim' : 'Não'}
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
              {isSelected ? 'Fechar Histórico' : 'Ver Histórico'}
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
                    value={user.authorized ? 'Sim' : 'Não'}
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
