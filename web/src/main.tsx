import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { AppProviders } from './app/providers'
import { router } from './app/router'
import './index.css'
import { worker } from './mocks/browser'

async function startApplication() {
  if (import.meta.env.VITE_USE_MOCKS === 'true') {
    await worker.start()
  }

  const rootElement = document.getElementById('root')
  if (!rootElement) {
    throw new Error('Не найден корневой элемент приложения.')
  }

  createRoot(rootElement).render(
    <StrictMode>
      <AppProviders>
        <RouterProvider router={router} />
      </AppProviders>
    </StrictMode>,
  )
}

void startApplication()
