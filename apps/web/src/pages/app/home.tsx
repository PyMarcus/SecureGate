import { useSessionStore } from '@/stores/session-store'

export const Home = () => {
  const { session } = useSessionStore()

  return (
    <section>
      <h1>Home</h1>
      <p>{session?.user.name}</p>
    </section>
  )
}
