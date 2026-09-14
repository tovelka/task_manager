export interface RegisterRequest {
  email: string
  password: string
  is_sandbox?: boolean
  invite_code?: string
  agree_terms: boolean
  understand_risks: boolean
  agree_data_processing: boolean
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  message?: string
}

export interface RefreshResponse {
  message?: string
}

export interface UserResponse {
  id: number
  username: string
  email: string
  created_at: string
}

export interface UserResponse {
  username: string
  email: string
  password: string
}

export interface EventSet {
  title: string
  description: string
  starts_at: string
  ends_at: string
}

export interface EventResponse {
  id: number
  title: string
  description: string
  starts_at: string
  ends_at: string
}

export interface EventListResponse {
  events: EventResponse[]
  count: number
}