import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useEffect, type PropsWithChildren } from 'react'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

export function AppProviders({ children }: PropsWithChildren) {
  useEffect(() => {
    const clearUserCache = () => queryClient.clear()
    window.addEventListener('auth:changed', clearUserCache)
    return () => window.removeEventListener('auth:changed', clearUserCache)
  }, [])

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}
