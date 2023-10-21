import { useSessionStore } from '@/stores/session-store'

export const Home = () => {
  const { session, clearSession } = useSessionStore()

  return (
    <section>
      <h1>Home</h1>

      <p>
        user: <strong>{session?.user}</strong>
      </p>
      <p>
        token: <strong>{session?.token}</strong>
      </p>

      <button onClick={clearSession}>Logout</button>
    </section>
  )
}
