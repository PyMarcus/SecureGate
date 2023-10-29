import { Button } from '@/components/ui/button'
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Link } from 'react-router-dom'

export const NotFound = () => {
  return (
    <div className="grid flex-1 place-items-center">
      <Card className="border-transparent sm:border-border w-full max-w-sm">
        <CardHeader>
          <CardTitle>404 - Page not found</CardTitle>
          <CardDescription>
            The page you are looking for does not exist.
          </CardDescription>
        </CardHeader>

        <CardFooter>
          <Button variant="outline" className="w-full" asChild>
            <Link to="/">Go back home</Link>
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
