import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { GearSix, SignOut, User } from '@phosphor-icons/react'
import { useNavigate } from 'react-router-dom'

interface UserNavProps {
  name: string
  email: string
  avatar?: string
  onSignOut: () => void
}

export const UserNav = ({
  name,
  email,
  avatar = '',
  onSignOut,
}: UserNavProps) => {
  const navigate = useNavigate()

  const handleNavigateToProfile = () => navigate('/profile')
  const handleNavigateToPreferences = () => navigate('/preferences')

  const avatarFallback = name
    .split(' ')
    .map((n) => n[0])
    .join('')

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-11 w-11 rounded-full">
          <Avatar className="h-11 w-11">
            <AvatarImage src={avatar} alt={name} />
            <AvatarFallback>{avatarFallback}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <div className="md:hidden">
          <DropdownMenuLabel className="font-normal">
            <div className="flex flex-col space-y-1">
              <p className="text-sm font-medium leading-none">{name}</p>
              <p className="text-xs leading-none text-muted-foreground">
                {email}
              </p>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
        </div>
        <DropdownMenuGroup>
          <DropdownMenuItem onClick={handleNavigateToProfile}>
            <span>Profile</span>
            <DropdownMenuShortcut>
              <User />
            </DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={handleNavigateToPreferences}>
            <span>Preferences</span>
            <DropdownMenuShortcut>
              <GearSix />
            </DropdownMenuShortcut>
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={onSignOut}>
          <span>Sign out</span>
          <DropdownMenuShortcut>
            <SignOut />
          </DropdownMenuShortcut>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
