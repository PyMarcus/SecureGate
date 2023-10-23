import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface Session {
  user: User
  token: string
}

interface SessionState {
  session: Session | null
  setSession: (session: Session) => void
  clearSession: () => void
}

export const useSessionStore = create<SessionState>()(
  devtools(
    persist(
      (set) => ({
        session: null,
        setSession: (session) => set({ session }),
        clearSession: () => set({ session: null }),
      }),
      {
        name: 'secure_gate::session-store',
        getStorage: () => localStorage,
        version: 1,
      },
    ),
  ),
)
