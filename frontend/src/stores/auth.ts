import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { API_ENDPOINTS } from '../config/api'

export interface User {
  id: string
  email: string
  fullname: string
  address: string
  pin_code: string
  is_admin: boolean
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<User | null>(null)
  const isAuthenticated = computed(() => !!currentUser.value)
  const isAdmin = computed(() => currentUser.value?.is_admin || false)

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch(API_ENDPOINTS.AUTH.LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })
      
      const data = await response.json()
      
      if (data.success) {
        currentUser.value = data.user
        localStorage.setItem('currentUser', JSON.stringify(data.user))
        return true
      }
      return false
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }

  const signup = async (userData: Omit<User, 'id' | 'is_admin' | 'created_at'> & { password: string }): Promise<boolean> => {
    try {
      const response = await fetch(API_ENDPOINTS.AUTH.REGISTER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      
      const data = await response.json()
      
      if (data.success) {
        currentUser.value = data.user
        localStorage.setItem('currentUser', JSON.stringify(data.user))
        return true
      }
      return false
    } catch (error) {
      console.error('Signup error:', error)
      return false
    }
  }

  const logout = () => {
    currentUser.value = null
    localStorage.removeItem('currentUser')
  }

  const initializeAuth = () => {
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      try {
        currentUser.value = JSON.parse(savedUser)
      } catch {
        localStorage.removeItem('currentUser')
      }
    }
  }

  return {
    currentUser,
    isAuthenticated,
    isAdmin,
    login,
    signup,
    logout,
    initializeAuth
  }
})