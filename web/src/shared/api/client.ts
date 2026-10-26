export type ValidationIssue = {
  loc?: Array<string | number>
  msg?: string
  type?: string
}

export class ApiError extends Error {
  readonly status: number
  readonly fieldErrors: Record<string, string>

  constructor(message: string, status: number, fieldErrors: Record<string, string> = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.fieldErrors = fieldErrors
  }
}

const baseURL = '/api/v1'

function getErrorMessage(detail: unknown): { message: string; fieldErrors: Record<string, string> } {
  if (typeof detail === 'string') {
    return { message: detail, fieldErrors: {} }
  }

  if (Array.isArray(detail)) {
    const fieldErrors: Record<string, string> = {}
    const messages = detail.flatMap((item: ValidationIssue) => {
      if (typeof item.msg !== 'string') return []
      const field = item.loc?.at(-1)
      if (typeof field === 'string' && field !== 'body') {
        fieldErrors[field] = item.msg
      }
      return [item.msg]
    })
    return { message: messages.join(' '), fieldErrors }
  }

  return { message: 'Не удалось выполнить запрос.', fieldErrors: {} }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  headers.set('Accept', 'application/json')
  if (init.body !== undefined) {
    headers.set('Content-Type', 'application/json')
  }

  const token = localStorage.getItem('access_token')
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${baseURL}${path}`, { ...init, headers })
  if (response.status === 401 && token) {
    localStorage.removeItem('access_token')
    window.dispatchEvent(new Event('auth:unauthorized'))
  }

  if (!response.ok) {
    let detail: unknown
    try {
      const body: unknown = await response.json()
      if (typeof body === 'object' && body !== null && 'detail' in body) {
        detail = body.detail
      }
    } catch {
      detail = undefined
    }
    const error = getErrorMessage(detail)
    throw new ApiError(error.message, response.status, error.fieldErrors)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}
