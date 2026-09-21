import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/full'
import type { UserResponse, LoginRequest, RegisterRequest } from '@/types'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserResponse | null>(null)
  const loading = ref(false)
  const initialized = ref(false)

  const isAuthenticated = computed(() => !!user.value)

  function clearAuthState() {
    user.value = null
  }

  async function login(credentials: LoginRequest) {
    loading.value = true
    try {
      await authApi.login(credentials)
      await fetchUser()
      router.push('/home')
    } finally {
      loading.value = false
    }
  }

  async function register(data: RegisterRequest) {
    loading.value = true
    try {
      const response = await authApi.register(data)
      router.push('/home')
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch {
    }
    clearAuthState()
    router.push('/login')
  }

  async function fetchUser(): Promise<boolean> {
    try {
      const { data } = await authApi.getMe() // Fixed this line
      user.value = data
      return true
    } catch {
      user.value = null
      return false
    }
  }

  async function initAuth() {
    if (initialized.value) return
    
    initialized.value = true
    loading.value = true
    
    try {
      await fetchUser()
    } finally {
      loading.value = false
    }
  }

  const initializeAuth = () => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem('user')

    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
  }

  return {
    user,
    loading,
    initialized,
    isAuthenticated,
    clearAuthState,
    login,
    register,
    logout,
    fetchUser,
    initAuth,
    initializeAuth
  }
})