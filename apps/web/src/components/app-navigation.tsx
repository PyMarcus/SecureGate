import { cn } from '@/lib/utils'
import { APP_PAGES } from '@/routes/app-pages'
import { NavLink } from 'react-router-dom'

export const AppNavigation = () => {
  return (
    <nav className="flex-1 hidden md:block">
      <ul className="flex gap-4">
        {APP_PAGES.map(({ name, path }) => (
          <li key={path}>
            <NavLink
              to={path}
              className={({ isActive }) =>
                cn(
                  'text-sm font-medium transition-colors hover:text-muted-foreground leading-none',
                  isActive ? 'text-tertiary' : 'text-primary',
                )
              }
            >
              {name}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
