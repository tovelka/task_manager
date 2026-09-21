import axios from 'axios'
import type { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
  withCredentials: true,
})

const AUTH_PATHS = [
  '/auth/login',
  '/auth/register', 
  '/auth/refresh',
  '/auth/logout',
]

let isRefreshing = false

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    const is401 = error.response?.status === 401
    const isAuthEndpoint = AUTH_PATHS.some(p => originalRequest?.url?.includes(p))
    const alreadyRetried = originalRequest?._retry === true

    if (is401 && !isAuthEndpoint && !alreadyRetried && !isRefreshing) {
      originalRequest._retry = true
      isRefreshing = true

      try {
        await apiClient.post('/auth/refresh', {})
        
        isRefreshing = false
        
        return apiClient(originalRequest)
      } catch (refreshError) {
        isRefreshing = false
        
        const { useAuthStore } = await import('@/stores/auth')
        const authStore = useAuthStore()
        authStore.clearAuthState()
        
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient




