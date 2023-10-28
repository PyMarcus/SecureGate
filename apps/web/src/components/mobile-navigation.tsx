import { cn } from '@/lib/utils'
import { APP_PAGES } from '@/routes/app-pages'
import { NavLink } from 'react-router-dom'

export const MobileNavigation = () => {
  return (
    <nav className="md:hidden w-full py-4 px-6">
      <ul className="flex gap-4 justify-around">
        {APP_PAGES.map(({ icon, path }) => (
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
              {icon}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
