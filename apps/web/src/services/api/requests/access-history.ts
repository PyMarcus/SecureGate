import {
  GetDeviceHistoryRequest,
  GetUserAccessHistoryRequest,
} from '@/@types/api/request'
import { GetAccessHistoryResponse } from '@/@types/api/response'
import { api } from '@/services/api/instance'
import { QueryFunctionContext, useQuery } from 'react-query'

const ACCESS_HISTORY_ENDPOINT = '/history'

const getDeviceAccessHistoryRequest = async (ctx: QueryFunctionContext) => {
  const [, deviceId, startDate, endDate] = ctx.queryKey

  const response = await api.get<GetAccessHistoryResponse>(
    `${ACCESS_HISTORY_ENDPOINT}/device/${deviceId}`,
    {
      params: {
        date_ini: startDate,
        date_end: endDate,
      },
    },
  )
  return response.data
}

export const useDeviceAccessHistory = ({
  deviceId,
  startDate,
  endDate,
}: GetDeviceHistoryRequest) => {
  return useQuery(
    ['deviceAccessHistory', deviceId, startDate, endDate],
    getDeviceAccessHistoryRequest,
  )
}

const getUserAccessHistoryRequest = async (ctx: QueryFunctionContext) => {
  const [, userId] = ctx.queryKey
  const response = await api.get<GetAccessHistoryResponse>(
    `${ACCESS_HISTORY_ENDPOINT}/${userId}`,
  )
  return response.data
}

export const useUserAccessHistory = ({
  userId,
}: GetUserAccessHistoryRequest) => {
  return useQuery(['userAccessHistory', userId], getUserAccessHistoryRequest)
}
