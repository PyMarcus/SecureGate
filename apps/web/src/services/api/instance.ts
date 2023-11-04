import axios from 'axios'

const { VITE_API_URL, VITE_BOARD_API_URL } = import.meta.env

export const serverApi = axios.create({
  baseURL: VITE_API_URL,
})

export const deviceApi = axios.create({
  baseURL: VITE_BOARD_API_URL,
})
