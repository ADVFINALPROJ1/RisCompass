import React, { createContext, useState, useEffect, useCallback, useContext } from 'react'
import authApi from '../api/authApi'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    setUser(null)
    setIsAuthenticated(false)
  }, [])

  const login = useCallback((userData, accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    localStorage.setItem('user', JSON.stringify(userData))
    setUser(userData)
    setIsAuthenticated(true)
  }, [])

  const register = useCallback(
    async (registrationData) => {
      setLoading(true)
      try {
        const response = await authApi.register(registrationData)
        const { user: userData, access, refresh } = response.data
        login(userData, access, refresh)
        return response.data
      } finally {
        setLoading(false)
      }
    },
    [login],
  )

  useEffect(() => {
    const initializeAuth = async () => {
      const accessToken = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')

      if (!accessToken || !refreshToken) {
        setLoading(false)
        return
      }

      try {
        const response = await authApi.getMe()
        setUser(response.data)
        setIsAuthenticated(true)
      } catch (error) {
        console.error('Failed to load user session:', error)
        logout()
      } finally {
        setLoading(false)
      }
    }

    initializeAuth()
  }, [logout])

  return (
    <AuthContext.Provider
      value={{ user, loading, isAuthenticated, login, logout, register }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
