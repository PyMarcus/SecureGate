import { CreateAdminRequest, GetAdminsRequest } from '@/@types/api/request'
import { CreateAdminResponse, GetAdminsResponse } from '@/@types/api/response'
import { queryClient } from '@/lib/react-query/client'
import { serverApi } from '@/services/api/instance'
import { useAdminStore } from '@/stores/admin-store'
import { QueryFunctionContext, useMutation, useQuery } from 'react-query'

const ADMINS_ENDPOINT = '/admins'

export const createAdminRequest = async (data: CreateAdminRequest) => {
  const response = await serverApi.post<CreateAdminResponse>(
    ADMINS_ENDPOINT,
    data,
  )
  return response.data
}

export const useCreateAdmin = () => {
  return useMutation('createAdmin', createAdminRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('userAdmins')
    },
  })
}

const getUserAdmins = async (ctx: QueryFunctionContext) => {
  const [, rootId] = ctx.queryKey
  const response = await serverApi.get<GetAdminsResponse>(
    `${ADMINS_ENDPOINT}/${rootId}`,
  )
  return response.data
}

export const useUserAdmins = ({ rootId }: GetAdminsRequest) => {
  const { setAdmins } = useAdminStore()

  return useQuery(['userAdmins', rootId], getUserAdmins, {
    onSuccess: (data) => {
      if (data.success) {
        setAdmins(data.data)
      }
    },
  })
}
