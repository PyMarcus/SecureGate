import { Button } from '@/components/ui/button'
import '@/styles/globals.css'

export const App = () => {
  const handleClick = () => console.log('clicked')

  return (
    <h1 className="bg-orange-400">
      SecureGate
      <Button onClick={handleClick}>Click me</Button>
    </h1>
  )
}
