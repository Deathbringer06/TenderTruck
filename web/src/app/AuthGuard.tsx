import { useEffect, useState } from 'react'
import { Navigate, Outlet } from 'react-router-dom'

export function AuthGuard() {
  const [hasToken, setHasToken] = useState(() => Boolean(localStorage.getItem('access_token')))

  useEffect(() => {
    const refreshTokenState = () => setHasToken(Boolean(localStorage.getItem('access_token')))
    window.addEventListener('storage', refreshTokenState)
    window.addEventListener('auth:unauthorized', refreshTokenState)
    window.addEventListener('auth:changed', refreshTokenState)
    return () => {
      window.removeEventListener('storage', refreshTokenState)
      window.removeEventListener('auth:unauthorized', refreshTokenState)
      window.removeEventListener('auth:changed', refreshTokenState)
    }
  }, [])

  return hasToken ? <Outlet /> : <Navigate to="/login" replace />
}
