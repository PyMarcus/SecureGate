import { AccessHistory } from '@/@types/schemas/access-history'
import { Device } from '@/@types/schemas/device'
import { create } from 'zustand'

interface DeviceState {
  devices: Device[]
  setDevices: (devices: Device[]) => void
  currentDevice: Device | null
  setCurrentDevice: (device: Device) => void

  deviceAccessHistory: AccessHistory[]
  setDeviceAccessHistory: (deviceAccessHistory: AccessHistory[]) => void

  isLoadingDevices: boolean
  setIsLoadingDevices: (isLoadingDevices: boolean) => void
}

export const useDeviceStore = create<DeviceState>((set) => ({
  devices: [],
  setDevices: (devices) => set({ devices }),
  currentDevice: null,
  setCurrentDevice: (currentDevice) => set({ currentDevice }),

  deviceAccessHistory: [],
  setDeviceAccessHistory: (deviceAccessHistory) => set({ deviceAccessHistory }),

  isLoadingDevices: false,
  setIsLoadingDevices: (isLoadingDevices) => set({ isLoadingDevices }),
}))
