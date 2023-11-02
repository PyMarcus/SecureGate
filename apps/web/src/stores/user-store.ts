import { User } from '@/@types/schemas/user'
import { create } from 'zustand'

interface DeviceState {
  users: User[]
  setUsers: (users: User[]) => void
  selectedUser: User | null
  setSelectedUser: (user: User) => void
  removeSelectedUser: () => void

  isLoadingUsers: boolean
  setIsLoadingUsers: (isLoadingUsers: boolean) => void
}

export const useUserStore = create<DeviceState>((set) => ({
  users: [],
  setUsers: (users) => set({ users }),
  selectedUser: null,
  setSelectedUser: (selectedUser) => set({ selectedUser }),
  removeSelectedUser: () => set({ selectedUser: null }),

  isLoadingUsers: false,
  setIsLoadingUsers: (isLoadingUsers) => set({ isLoadingUsers }),
}))
