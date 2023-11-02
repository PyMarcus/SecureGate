import {
  getAllDevicesRequest,
  getDeviceUsersRequest,
} from '@/services/api/requests/devices'
import { useDeviceStore } from '@/stores/device-store'
import { useUserStore } from '@/stores/user-store'
import { ReactNode, createContext, useContext, useEffect } from 'react'
import { useQuery } from 'react-query'

interface DeviceContextType {}

interface DeviceProviderProps {
  children: ReactNode
}

export const DeviceContext = createContext({} as DeviceContextType)

export const DeviceProvider = ({ children }: DeviceProviderProps) => {
  const { currentDevice, setDevices, setIsLoadingDevices } = useDeviceStore()

  const { setUsers, setIsLoadingUsers } = useUserStore()

  const getDevices = () => getAllDevicesRequest()
  const { isLoading: isLoadingDevices, data: devicesResponse } = useQuery(
    'allDevices',
    getDevices,
  )

  useEffect(() => {
    setIsLoadingDevices(isLoadingDevices)
    if (devicesResponse && devicesResponse.success) {
      setDevices(devicesResponse.data)
    }
  }, [devicesResponse, isLoadingDevices, setDevices, setIsLoadingDevices])

  const getDeviceUsers = () =>
    getDeviceUsersRequest({
      deviceId: currentDevice!.id,
    })

  const { isLoading: isLoadingUsers, data: usersResponse } = useQuery(
    'deviceUsers',
    getDeviceUsers,
    { enabled: !!currentDevice },
  )

  useEffect(() => {
    setIsLoadingUsers(isLoadingUsers)
    if (usersResponse && usersResponse.success) {
      setUsers(usersResponse.data)
    }
  }, [isLoadingUsers, usersResponse, setIsLoadingUsers, setUsers])

  return <DeviceContext.Provider value={{}}>{children}</DeviceContext.Provider>
}

export const useDevice = () => useContext(DeviceContext)
