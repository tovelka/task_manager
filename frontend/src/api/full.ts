import apiClient from './client'
import type {
  UserResponse,
  LoginRequest,
  RegisterRequest,
  EventSet,
  EventResponse,
  EventListResponse
} from '@/types'

export const authApi = {
  login: (credentials: LoginRequest) => apiClient.post('/auth/login/', credentials),
  register: (data: RegisterRequest) => apiClient.post('/auth/register/', data),
  logout: () => apiClient.post('/auth/logout/'),
  getMe: () => apiClient.get<UserResponse>('/auth/me'),
}
export const eventsApi = {
  getAll: () => apiClient.get<EventListResponse>('/events/'),
  getById: (id: number) => apiClient.get<EventResponse>(`/events/${id}`),
  create: (data: EventSet) => apiClient.post<EventResponse>('/events/', data),
  update: (id: number, data: EventSet) => apiClient.patch<EventResponse>(`/events/${id}`, data),
  delete: (id: number) => apiClient.delete(`/events/${id}`),
}
