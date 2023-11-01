import { CreateUserRequest } from '@/@types/api/request'
import { GetAllMembersResponse } from '@/@types/api/response'
import { api } from '@/services/api/instance'
import { useMutation, useQuery } from 'react-query'

const USERS_ENDPOINT = '/users'

const getAllUsersRequest = async () => {
  const response = await api.get<GetAllMembersResponse>(USERS_ENDPOINT)
  return response.data
}

export const useAllUsers = () => {
  return useQuery('allUsers', getAllUsersRequest, {})
}

const createUserRequest = async (data: CreateUserRequest) => {
  const response = await api.post<GetAllMembersResponse>(USERS_ENDPOINT, data)
  return response.data
}

export const useCreateUser = () => {
  return useMutation('createUser', createUserRequest)
}
