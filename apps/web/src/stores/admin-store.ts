import { Admin } from '@/@types/schemas/admin'
import { create } from 'zustand'

interface AdminState {
  admins: Admin[]
  setAdmins: (admins: Admin[]) => void

  isLoadingAdmins: boolean
  setIsLoadingAdmins: (isLoadingAdmins: boolean) => void
}

export const useAdminStore = create<AdminState>((set) => ({
  admins: [],
  setAdmins: (admins) => set({ admins }),

  isLoadingAdmins: false,
  setIsLoadingAdmins: (isLoadingAdmins) => set({ isLoadingAdmins }),
}))
