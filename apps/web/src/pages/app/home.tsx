import { usePreferencesStore } from '@/stores/preferences-store'
import { useSessionStore } from '@/stores/session-store'

export const Home = () => {
  const { session, clearSession } = useSessionStore()
  const { theme } = usePreferencesStore()

  console.log(theme)

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
