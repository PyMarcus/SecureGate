import { cn } from '@/lib/utils'
import { APP_PAGES } from '@/routes/app-pages'
import { NavLink } from 'react-router-dom'

interface AppNavigationProps {
  mobile?: boolean
}

export const AppNavigation = ({ mobile }: AppNavigationProps) => {
  return (
    <nav className={cn('flex-1', mobile && 'w-full py-4 px-6')}>
      <ul className={cn('flex gap-4', mobile && 'justify-around')}>
        {APP_PAGES.map(({ name, path, icon }) => (
          <li key={path}>
            <NavLink
              to={path}
              className={({ isActive }) =>
                cn(
                  'text-sm font-medium transition-colors hover:text-primary/80 leading-none',
                  isActive
                    ? 'text-primary hover:text-primary'
                    : 'text-muted-foreground',
                )
              }
            >
              {mobile ? icon : name}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
