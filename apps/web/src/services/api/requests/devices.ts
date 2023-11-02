import { CreateDeviceRequest } from '@/@types/api/request'
import {
  CreateDeviceResponse,
  GetAllDevicesResponse,
  GetDeviceUsersResponse,
} from '@/@types/api/response'
import { queryClient } from '@/lib/react-query/client'
import { api } from '@/services/api/instance'
import { QueryFunctionContext, useMutation, useQuery } from 'react-query'

const DEVICES_ENDPOINT = '/devices'

const getAllDevicesRequest = async () => {
  const response = await api.get<GetAllDevicesResponse>(DEVICES_ENDPOINT)
  return response.data
}

export const useAllDevices = () => {
  return useQuery('allDevices', getAllDevicesRequest)
}

const createDeviceRequest = async (data: CreateDeviceRequest) => {
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

const getDeviceUsers = async (ctx: QueryFunctionContext) => {
  const [, deviceId] = ctx.queryKey
  const response = await api.get<GetDeviceUsersResponse>(
    `${DEVICES_ENDPOINT}/${deviceId}/users`,
  )
  return response.data
}

export const useDeviceUsers = () => {
  return useQuery('deviceUsers', getDeviceUsers, {})
}
