import {
  GetAllAccessHistoryRequest,
  GetUserAccessHistoryRequest,
} from '@/@types/api/request'
import { api } from '@/services/api/instance'
import { useQuery } from 'react-query'

const ACCESS_HISTORY_ENDPOINT = '/history'

const getAllAccessHistoryRequest = async () => {
  const response = await api.get<GetAllAccessHistoryRequest>(
    ACCESS_HISTORY_ENDPOINT,
  )
  return response.data
}

export const useAllAccessHistory = () => {
  return useQuery('allAccessHistory', getAllAccessHistoryRequest, {})
}

const getUserAccessHistoryRequest = async () => {
  const response = await api.get<GetUserAccessHistoryRequest>(
    ACCESS_HISTORY_ENDPOINT,
  )
  return response.data
}

export const useUserAccessHistory = () => {
  return useQuery('userAccessHistory', getUserAccessHistoryRequest, {})
}
