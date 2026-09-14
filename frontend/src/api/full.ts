import apiClient from './client'
import type {
    RegisterRequest,
    LoginRequest,
    EventListResponse,
    EventResponse,
    EventSet
} from '@/types'

export const authApi = {
    register(data: RegisterRequest) {
        return apiClient.post('/auth/register', data)
    },

    login(data: LoginRequest) {
        return apiClient.post('/auth/login', data)
    },

    refresh() {
        return apiClient.post('/auth/refresh_token', {})
    },

    logout() {
        return apiClient.post('/auth/logout', {})
    },
}

export const eventsApi = {
    get_event(event_id: number): Promise<{ data: EventResponse }> {
        return apiClient.get(`/auth/events/${event_id}`)
    },

    get_all(): Promise<{ data: EventListResponse }>{
        return apiClient.get('/auth/events')
    },

    update(event_id: number, event_data: EventSet): Promise<{ data: EventResponse }> {
        return apiClient.patch(`/auth/events/${event_id}`, event_data)
    },

    create(event_data: EventSet): Promise<{ data: EventResponse }> {
        return apiClient.post('/auth/events/', event_data)
    },

    delete(event_id: number): Promise<{ data: boolean }> {
        return apiClient.delete(`/auth/events/${event_id}`)
    },
}