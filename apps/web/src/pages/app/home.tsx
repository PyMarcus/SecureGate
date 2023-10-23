import { Button } from '@/components/ui/button'
import { useSessionStore } from '@/stores/session-store'

export const Home = () => {
  const { session, clearSession } = useSessionStore()

  const hasSession = !!session

  return (
    <section>
      <h1>Home</h1>
      <p>{session?.user.name}</p>
      {hasSession && <Button onClick={clearSession}>Sign Out</Button>}
    </section>
  )
}
