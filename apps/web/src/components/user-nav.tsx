import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
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
import { Theme, usePreferencesStore } from '@/stores/preferences-store'
import { Moon, SignOut, Sun, User } from '@phosphor-icons/react'
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
  const { theme, setTheme } = usePreferencesStore()
  const handleThemeChange = (theme: string) => setTheme(theme as Theme)

  const navigate = useNavigate()
  const handleNavigateToProfile = () => navigate('/profile')

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
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuSub>
          <DropdownMenuSubTrigger>Theme</DropdownMenuSubTrigger>
          <DropdownMenuPortal>
            <DropdownMenuSubContent>
              <DropdownMenuRadioGroup
                value={theme}
                onValueChange={handleThemeChange}
              >
                <DropdownMenuRadioItem value="light">
                  Light
                  <DropdownMenuShortcut>
                    <Sun />
                  </DropdownMenuShortcut>
                </DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="dark">
                  Dark
                  <DropdownMenuShortcut>
                    <Moon />
                  </DropdownMenuShortcut>
                </DropdownMenuRadioItem>
              </DropdownMenuRadioGroup>
            </DropdownMenuSubContent>
          </DropdownMenuPortal>
        </DropdownMenuSub>
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
