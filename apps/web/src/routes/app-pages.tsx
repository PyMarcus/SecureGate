import { SquaresFour, User } from '@phosphor-icons/react'

export interface Page {
  name: string
  path: string
  icon: JSX.Element
}

export const APP_PAGES: Page[] = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: <SquaresFour size={26} />,
  },
  {
    name: 'Profile',
    path: '/profile',
    icon: <User size={26} />,
  },
]
