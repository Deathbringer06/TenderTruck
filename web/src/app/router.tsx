import { useEffect, useState } from 'react'
import { createBrowserRouter, Navigate, Outlet } from 'react-router-dom'
import { CabinetLayout } from '../features/cabinet/CabinetLayout'
import { ProfilePage } from '../features/profile/ProfilePage'
import { DevLoginPage as RealBackendDevLoginPage } from './DevLoginPage'

const mocksEnabled = import.meta.env.VITE_USE_MOCKS === 'true'
const realBackendDevLoginEnabled = import.meta.env.DEV && !mocksEnabled

export function AuthGuard() {
  const [hasToken, setHasToken] = useState(
    () => Boolean(localStorage.getItem('access_token')),
  )

  useEffect(() => {
    const refreshTokenState = () => setHasToken(Boolean(localStorage.getItem('access_token')))
    window.addEventListener('storage', refreshTokenState)
    window.addEventListener('auth:unauthorized', refreshTokenState)
    return () => {
      window.removeEventListener('storage', refreshTokenState)
      window.removeEventListener('auth:unauthorized', refreshTokenState)
    }
  }, [])

  if (!hasToken) {
    if (mocksEnabled) {
      return <Navigate to="/dev-login" replace />
    }
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}

function MockDevLoginPage() {
  function signIn(role: 'zakazchik' | 'perevozchik') {
    localStorage.setItem('access_token', `dev-token:${role}`)
    window.location.assign('/cabinet/profile')
  }

  return (
    <main className="login-screen">
      <section className="login-card" aria-labelledby="dev-login-title">
        <span className="eyebrow">ТендерТрак · разработка</span>
        <h1 id="dev-login-title">Вход для разработки</h1>
        <p className="muted-copy">Эта страница доступна только для разработки.</p>
        <div className="login-actions">
          <button className="button button-primary" onClick={() => signIn('zakazchik')} type="button">
            Войти как Заказчик
          </button>
          <button className="button button-secondary" onClick={() => signIn('perevozchik')} type="button">
            Войти как Перевозчик
          </button>
        </div>
      </section>
    </main>
  )
}

const routes = [
  {
    path: '/',
    element: <Navigate to="/cabinet/profile" replace />,
  },
  {
    path: '/cabinet',
    element: <AuthGuard />,
    children: [
      {
        element: <CabinetLayout />,
        children: [
          { index: true, element: <Navigate to="profile" replace /> },
          { path: 'profile', element: <ProfilePage /> },
        ],
      },
    ],
  },
  ...(realBackendDevLoginEnabled
    ? [{ path: '/dev-login', element: <RealBackendDevLoginPage /> }]
    : []),
  ...(import.meta.env.DEV && mocksEnabled
    ? [{ path: '/dev-login', element: <MockDevLoginPage /> }]
    : []),
  { path: '/login', element: <Navigate to="/dev-login" replace /> },
  { path: '*', element: <Navigate to="/cabinet/profile" replace /> },
]

export const router = createBrowserRouter(routes)
