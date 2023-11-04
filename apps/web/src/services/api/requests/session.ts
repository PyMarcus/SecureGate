import { SignInRequest, SignUpRequest } from '@/@types/api/request'
import { SignInResponse } from '@/@types/api/response'
import { serverApi } from '@/services/api/instance'
import { useMutation, useQuery } from 'react-query'

const SESSIONS_ENDPOINT = '/session'

export const signInRequest = async (data: SignInRequest) => {
  const response = await serverApi.post<SignInResponse>(
    `${SESSIONS_ENDPOINT}/signin`,
    data,
  )
  return response.data
}

export const useSignIn = () => {
  return useMutation('signin', signInRequest)
}

export const signUpRequest = async (data: SignUpRequest) => {
  const response = await serverApi.post<SignInResponse>(
    `${SESSIONS_ENDPOINT}/signup`,
    data,
  )
  return response.data
}

export const useSignUp = () => {
  return useMutation('signup', signUpRequest)
}

export const healthRequest = async () => {
  const response = await serverApi.get('/management/health')
  return response.data
}

export const useHealth = () => {
  return useQuery('health', healthRequest)
}
