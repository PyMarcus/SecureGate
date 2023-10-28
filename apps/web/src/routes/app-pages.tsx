import { Gear, SquaresFour, User } from '@phosphor-icons/react'

export const APP_PAGES = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: <SquaresFour size={26} />,
  },
  {
    name: 'Preferences',
    path: '/preferences',
    icon: <Gear size={26} />,
  },
  {
    name: 'Profile',
    path: '/profile',
    icon: <User size={26} />,
  },
]
