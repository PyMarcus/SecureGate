import { CreateUserRequest } from '@/@types/api/request'
import { CreateUserResponse } from '@/@types/api/response'
import { queryClient } from '@/lib/react-query/client'
import { api } from '@/services/api/instance'
import { useMutation } from 'react-query'

const USERS_ENDPOINT = '/users'

const createUserRequest = async (data: CreateUserRequest) => {
  const response = await api.post<CreateUserResponse>(USERS_ENDPOINT, data)
  return response.data
}

export const useCreateUser = () => {
  return useMutation('createUser', createUserRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('allUsers')
    },
  })
}
