import {
  CreateDeviceRequest,
  GetDeviceHistoryRequest,
  GetDeviceUsersRequest,
} from '@/@types/api/request'
import {
  CreateDeviceResponse,
  GetAccessHistoryResponse,
  GetAllDevicesResponse,
  GetDeviceUsersResponse,
} from '@/@types/api/response'
import { queryClient } from '@/lib/react-query/client'
import { api } from '@/services/api/instance'
import { useMutation } from 'react-query'

const DEVICES_ENDPOINT = '/devices'

export const getAllDevicesRequest = async () => {
  const response = await api.get<GetAllDevicesResponse>(DEVICES_ENDPOINT)
  return response.data
}

export const createDeviceRequest = async (data: CreateDeviceRequest) => {
  const response = await api.post<CreateDeviceResponse>(DEVICES_ENDPOINT, data)
  return response.data
}

export const useCreateDevice = () => {
  return useMutation('createDevice', createDeviceRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('allDevices')
    },
  })
}

export const getDeviceUsersRequest = async ({
  deviceId,
}: GetDeviceUsersRequest) => {
  const response = await api.get<GetDeviceUsersResponse>(
    `${DEVICES_ENDPOINT}/${deviceId}/users`,
  )
  return response.data
}

export const getDeviceAccessHistoryRequest = async ({
  deviceId,
  startDate,
  endDate,
}: GetDeviceHistoryRequest) => {
  const response = await api.get<GetAccessHistoryResponse>(
    `${DEVICES_ENDPOINT}/${deviceId}/history`,
    {
      params: {
        date_ini: startDate,
        date_end: endDate,
      },
    },
  )
  return response.data
}
