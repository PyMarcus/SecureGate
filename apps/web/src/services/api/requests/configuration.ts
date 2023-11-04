import { ConfigureDeviceRequest } from '@/@types/api/request'
import { ConfigureDeviceResponse } from '@/@types/api/response'
import { deviceApi } from '@/services/api/instance'
import { useMutation } from 'react-query'

const { VITE_BOARD_TOKEN } = import.meta.env

const configureDeviceRequest = async (data: ConfigureDeviceRequest) => {
  deviceApi.defaults.headers.Authorization = `Bearer ${VITE_BOARD_TOKEN}`

  const response = await deviceApi.post<ConfigureDeviceResponse>('', data)
  return response.data
}

export const useConfigureDevice = () => {
  return useMutation('configureDevice', configureDeviceRequest, {
    onError: (error) => {
      console.error(error)
    },
  })
}
