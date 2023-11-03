import {
  CreateUserRequest,
  GetUserAccessHistoryRequest,
} from '@/@types/api/request'
import {
  CreateUserResponse,
  GetAccessHistoryResponse,
} from '@/@types/api/response'
import { queryClient } from '@/lib/react-query/client'
import { api } from '@/services/api/instance'
import { QueryFunctionContext, useMutation, useQuery } from 'react-query'

const USERS_ENDPOINT = '/users'

export const createUserRequest = async (data: CreateUserRequest) => {
  const response = await api.post<CreateUserResponse>(USERS_ENDPOINT, data)
  return response.data
}

export const useCreateUser = () => {
  return useMutation('createUser', createUserRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('deviceUsers')
    },
  })
}

const getUserAccessHistoryRequest = async (ctx: QueryFunctionContext) => {
  const [, userId] = ctx.queryKey
  const response = await api.get<GetAccessHistoryResponse>(
    `${USERS_ENDPOINT}/${userId}/history`,
  )
  return response.data
}

export const useUserAccessHistory = ({
  userId,
}: GetUserAccessHistoryRequest) => {
  return useQuery(['userAccessHistory', userId], getUserAccessHistoryRequest)
}
