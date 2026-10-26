import { createBrowserRouter, Navigate } from 'react-router-dom'
import { AuthGuard } from './AuthGuard'
import { AuthPage } from './AuthPage'
import { CabinetLayout } from '../features/cabinet/CabinetLayout'
import { ProfilePage } from '../features/profile/ProfilePage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to={localStorage.getItem('access_token') ? '/cabinet/profile' : '/login'} replace />,
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
  { path: '/login', element: <AuthPage /> },
  { path: '/register', element: <AuthPage /> },
  { path: '*', element: <Navigate to="/" replace /> },
])
