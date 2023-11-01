import { SquaresFour, User } from '@phosphor-icons/react'

export interface Page {
  name: string
  path: string
  icon: JSX.Element
}

export const APP_PAGES: Page[] = [
  {
    name: 'Painel',
    path: '/painel',
    icon: <SquaresFour size={26} />,
  },
  {
    name: 'Perfil',
    path: '/perfil',
    icon: <User size={26} />,
  },
]
