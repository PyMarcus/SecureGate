import { CreateDeviceRequest } from '@/@types/api/request'
import {
  CreateDeviceResponse,
  GetAllDevicesResponse,
} from '@/@types/api/response'
import { queryClient } from '@/lib/react-query/client'
import { api } from '@/services/api/instance'
import { useMutation, useQuery } from 'react-query'

const DEVICES_ENDPOINT = '/devices'

const getAllDevicesRequest = async () => {
  const response = await api.get<GetAllDevicesResponse>(DEVICES_ENDPOINT)
  return response.data
}

export const useAllDevices = () => {
  return useQuery('allDevices', getAllDevicesRequest, {})
}

const createDeviceRequest = async (data: CreateDeviceRequest) => {
  const response = await api.post<CreateDeviceResponse>(DEVICES_ENDPOINT, data)
  return response.data
}

export const useCreateDevice = () => {
  return useMutation('createDevice', createDeviceRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('allUsers')
    },
  })
}
