import {
  CreateDeviceRequest,
  DeviceActivationRequest,
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
import { serverApi } from '@/services/api/instance'
import { QueryFunctionContext, useMutation, useQuery } from 'react-query'

const DEVICES_ENDPOINT = '/devices'

const getAllDevicesRequest = async () => {
  const response = await serverApi.get<GetAllDevicesResponse>(DEVICES_ENDPOINT)
  return response.data
}

export const useGetAllDevices = () =>
  useQuery('allDevices', getAllDevicesRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('deviceUsers')
      queryClient.invalidateQueries('deviceHistory')
    },
  })

export const createDeviceRequest = async (data: CreateDeviceRequest) => {
  const response = await serverApi.post<CreateDeviceResponse>(
    DEVICES_ENDPOINT,
    data,
  )
  return response.data
}

export const useCreateDevice = () => {
  return useMutation('createDevice', createDeviceRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('allDevices')
    },
  })
}

const getDeviceUsersRequest = async (ctx: QueryFunctionContext) => {
  const [, deviceId] = ctx.queryKey
  const response = await serverApi.get<GetDeviceUsersResponse>(
    `${DEVICES_ENDPOINT}/${deviceId}/users`,
  )
  return response.data
}

export const useDeviceUsers = ({ deviceId }: GetDeviceUsersRequest) => {
  return useQuery(['deviceUsers', deviceId], getDeviceUsersRequest)
}

export const getDeviceAccessHistoryRequest = async (
  ctx: QueryFunctionContext,
) => {
  const [, deviceId, date] = ctx.queryKey
  const response = await serverApi.get<GetAccessHistoryResponse>(
    `${DEVICES_ENDPOINT}/${deviceId}/history`,
    { params: { date } },
  )
  return response.data
}

export const useDeviceAccessHistory = ({
  deviceId,
  date,
}: GetDeviceHistoryRequest) => {
  return useQuery(
    ['deviceHistory', deviceId, date],
    getDeviceAccessHistoryRequest,
  )
}

const deviceActivationRequest = async ({
  deviceId,
  action,
}: DeviceActivationRequest) => {
  const response = await serverApi.post(
    `${DEVICES_ENDPOINT}/${deviceId}/activation`,
    {
      device_id: deviceId,
      action,
    },
  )
  return response.data
}

export const useDeviceActivation = () => {
  return useMutation('deviceActivation', deviceActivationRequest, {
    onError: (error) => {
      console.log(error)
    },
  })
}
