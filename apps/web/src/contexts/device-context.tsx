import { useAllDevices, useDeviceUsers } from '@/services/api/requests/devices'
import { useDeviceStore } from '@/stores/device-store'
import { useUserStore } from '@/stores/user-store'
import { ReactNode, createContext, useContext, useEffect } from 'react'

interface DeviceContextType {}

interface DeviceProviderProps {
  children: ReactNode
}

export const DeviceContext = createContext({} as DeviceContextType)

export const DeviceProvider = ({ children }: DeviceProviderProps) => {
  const { isLoading: isLoadingDevices, data: devicesResponse } = useAllDevices()
  const { setDevices, setIsLoadingDevices } = useDeviceStore()
  const hasDevices = devicesResponse && devicesResponse.success

  useEffect(() => {
    setIsLoadingDevices(isLoadingDevices)
    if (hasDevices) {
      setDevices(devicesResponse.data)
    }
  }, [
    hasDevices,
    devicesResponse,
    isLoadingDevices,
    setDevices,
    setIsLoadingDevices,
  ])

  const { data: response, isLoading: isLoadingUsers } = useDeviceUsers()
  const { setUsers, setIsLoadingUsers } = useUserStore()
  const hasUsers = response && response.success

  useEffect(() => {
    setIsLoadingUsers(isLoadingUsers)
    if (hasUsers) {
      setUsers(response.data)
    }
  }, [hasUsers, isLoadingUsers, response, setIsLoadingUsers, setUsers])

  // const {
  //   currentDevice,
  //   setDevices,
  //   setDeviceAccessHistory,
  //   setIsLoadingDevices,
  // } = useDeviceStore()
  // const { setUsers, setIsLoadingUsers } = useUserStore()

  // useEffect(() => {
  //   setIsLoadingDevices(isLoadingDevices)
  //   if (allDevices && allDevices.success) {
  //     setDevices(allDevices.data)
  //   }
  // }, [isLoadingDevices, allDevices, setDevices, setIsLoadingDevices])

  // const { data: response, isLoading: isLoadingUsers } = useAllUsers()

  // useEffect(() => {
  //   setIsLoadingUsers(isLoadingUsers)
  //   if (response && response.success) {
  //     setUsers(response.data)
  //   }
  // }, [isLoadingUsers, response, setIsLoadingUsers, setUsers])

  // const currentDate = new Date()
  // const twentyFourHoursAgo = sub(currentDate, { hours: 24 })

  // const { data: historyResponse } = useDeviceAccessHistory({
  //   deviceId: currentDevice?.id || '',
  //   startDate: format(twentyFourHoursAgo, 'yyyy-MM-dd HH:mm'),
  //   endDate: format(currentDate, 'yyyy-MM-dd HH:mm'),
  // })

  // if (historyResponse && historyResponse.success) {
  //   setDeviceAccessHistory(historyResponse.data)
  // }

  return <DeviceContext.Provider value={{}}>{children}</DeviceContext.Provider>
}

export const useDevice = () => useContext(DeviceContext)
