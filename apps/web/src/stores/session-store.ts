import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface Session {
  user: string
  token: string
}

interface BearState {
  session: Session | null
  setSession: (session: Session) => void
  clearSession: () => void
}

export const useSessionStore = create<BearState>()(
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
