import { Button } from '@/components/ui/button'
import { Link } from 'react-router-dom'

export const NotFound = () => {
  return (
    <div className="grid flex-1 place-items-center">
      <article className="text-center space-y-4">
        <h1 className="text-2xl font-semibold tracking-tight">
          Page not found
        </h1>
        <p className="text-sm text-muted-foreground">
          The page you are looking for does not exist.
        </p>
        <Button variant="outline" asChild>
          <Link to="/">Go back home</Link>
        </Button>
      </article>
    </div>
  )
}
