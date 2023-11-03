import { buttonVariants } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { Page } from '@/routes/app-pages'
import { NavLink } from 'react-router-dom'

interface SidebarNavProps {
  pages: Page[]
}
// hover:bg-accent hover:text-accent-foreground
export const SidebarNav = ({ pages }: SidebarNavProps) => {
  return (
    <nav>
      <ul>
        {pages.map(({ name, path, icon }) => (
          <li key={path}>
            <NavLink
              to={path}
              className={({ isActive }) =>
                cn(
                  buttonVariants({ variant: 'ghost' }),
                  isActive
                    ? 'text-primary hover:text-primary'
                    : 'text-muted-foreground',
                  'justify-start',
                )
              }
            >
              <span>{icon}</span>
              <span className="ml-2">{name}</span>
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
