import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

export type Theme = 'light' | 'dark'

interface PreferencesStates {
  theme: Theme
}

interface PreferencesSchema extends PreferencesStates {
  toggleTheme: () => void
  setTheme: (theme: Theme) => void
}

interface PreferencesStorage {
  state: PreferencesStates
  version: number
}

type StoredPreferences = PreferencesStorage | null

const STORAGE_KEY = 'secure_gate::preferences'

const getStoredPreferences = (): StoredPreferences => {
  const storedPreferences = localStorage.getItem(STORAGE_KEY)
  if (!storedPreferences) return null
  return JSON.parse(storedPreferences)
}

const getInitialTheme = (): Theme => {
  const storedPreferences = getStoredPreferences()
  const preferredIsDark = window.matchMedia(
    '(prefers-color-scheme: dark)',
  ).matches

  if (storedPreferences) return storedPreferences.state.theme
  if (preferredIsDark) return 'dark'
  return 'light'
}

export const usePreferencesStore = create<PreferencesSchema>()(
  devtools(
    persist(
      (set) => ({
        theme: getInitialTheme(),
        toggleTheme: () =>
          set((state) => ({
            theme: state.theme === 'light' ? 'dark' : 'light',
          })),
        setTheme: (theme) =>
          set(() => ({
            theme,
          })),
      }),
      {
        name: STORAGE_KEY,
        getStorage: () => localStorage,
        version: 1,
      },
    ),
  ),
)
