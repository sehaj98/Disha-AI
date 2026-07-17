import { createContext, useContext, useEffect, useState } from 'react'
import { API_URL } from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('disha_token'))
  const [student, setStudent] = useState(null)
  const [loading, setLoading] = useState(true)

  // Whenever we have a token (on load, or right after login/signup), fetch
  // the profile it belongs to. If the token is invalid/expired, log out.
  useEffect(() => {
    if (!token) {
      setStudent(null)
      setLoading(false)
      return
    }

    fetch(`${API_URL}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Session expired')
        return res.json()
      })
      .then(setStudent)
      .catch(() => {
        localStorage.removeItem('disha_token')
        setToken(null)
        setStudent(null)
      })
      .finally(() => setLoading(false))
  }, [token])

  async function login(email, password) {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Login failed')
    }
    const data = await res.json()
    localStorage.setItem('disha_token', data.access_token)
    setToken(data.access_token)
  }

  async function signup(payload) {
    const res = await fetch(`${API_URL}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Signup failed')
    }
    const data = await res.json()
    localStorage.setItem('disha_token', data.access_token)
    setToken(data.access_token)
  }

  function logout() {
    localStorage.removeItem('disha_token')
    setToken(null)
    setStudent(null)
  }

  return (
    <AuthContext.Provider value={{ token, student, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider')
  return ctx
}
