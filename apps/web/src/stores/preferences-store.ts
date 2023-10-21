import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

type Theme = 'light' | 'dark'
type Language = 'en-US' | 'pt-BR'

interface PreferencesStates {
  theme: Theme
  language: Language
}

interface PreferencesSchema extends PreferencesStates {
  toggleTheme: () => void
  toggleLanguage: () => void
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

const getInitialLanguage = (): Language => {
  const storedPreferences = getStoredPreferences()
  const preferredIsBR = navigator.language === 'pt-BR'

  if (storedPreferences) return storedPreferences.state.language
  if (preferredIsBR) return 'pt-BR'
  return 'en-US'
}

export const usePreferencesStore = create<PreferencesSchema>()(
  devtools(
    persist(
      (set) => ({
        theme: getInitialTheme(),
        language: getInitialLanguage(),
        toggleTheme: () =>
          set((state) => ({
            theme: state.theme === 'light' ? 'dark' : 'light',
          })),
        toggleLanguage: () =>
          set((state) => ({
            language: state.language === 'en-US' ? 'pt-BR' : 'en-US',
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
