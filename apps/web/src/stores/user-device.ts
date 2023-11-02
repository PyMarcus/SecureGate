import { Device } from '@/@types/schemas/device'
import { User } from '@/@types/schemas/user'
import { create } from 'zustand'

import { devtools, persist } from 'zustand/middleware'

interface DeviceState {
  isLoading: boolean
  currentDevice: Device | null
  selectedUser: User | null
  users: User[]

  setCurrentDevice: (device: Device) => void
  clearCurrentDevice: () => void
  setSelectedUser: (user: User) => void
  clearSelectedUser: () => void
  setUsers: (users: User[]) => void
  setIsLoading: (isLoading: boolean) => void
}

export const useDeviceStore = create<DeviceState>()(
  devtools(
    persist(
      (set) => ({
        isLoading: false,
        currentDevice: null,
        selectedUser: null,
        users: [],
        setCurrentDevice: (device) => set({ currentDevice: device }),
        clearCurrentDevice: () => set({ currentDevice: null }),
        setSelectedUser: (user) => set({ selectedUser: user }),
        clearSelectedUser: () => set({ selectedUser: null }),
        setUsers: (users) => set({ users }),
        setIsLoading: (isLoading) => set({ isLoading }),
      }),
      {
        name: 'secure_gate::device-store',
        getStorage: () => localStorage,
        version: 1,
      },
    ),
  ),
)
