export interface RegisterRequest {
  email: string
  username: string
  password: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  message?: string
}

export interface UserResponse {
  id: number
  username: string
  email: string
  created_at: string
}

export interface EventSet {
  title: string
  description?: string
  starts_at: string
  ends_at: string
}

export interface EventResponse {
  id: number
  title: string
  description?: string
  starts_at: string
  ends_at: string
  created_by_id: number
  created_at: string
}

export interface EventListResponse {
  events: EventResponse[]
  count: number
}