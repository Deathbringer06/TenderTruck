import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { ApiError, apiRequest } from '../shared/api/client'

type LoginResponse = { access_token: string; token_type: string }

export function DevLoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setPending(true)
    try {
      const token = await apiRequest<LoginResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      localStorage.setItem('access_token', token.access_token)
      navigate('/cabinet/profile', { replace: true })
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : 'Не удалось выполнить вход.')
    } finally {
      setPending(false)
    }
  }

  return (
    <main className="login-screen">
      <section className="login-card" aria-labelledby="dev-login-title">
        <span className="eyebrow">Временный инструмент разработки</span>
        <h1 id="dev-login-title">Вход в кабинет</h1>
        <form className="login-actions" onSubmit={handleSubmit}>
          <label className="field">
            <span className="field-label">Email</span>
            <input className="text-input" type="email" autoComplete="username" required value={email} onChange={(event) => setEmail(event.target.value)} />
          </label>
          <label className="field">
            <span className="field-label">Пароль</span>
            <input className="text-input" type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} />
          </label>
          {error && <p className="field-error" role="alert">{error}</p>}
          <button className="button button-primary" type="submit" disabled={pending}>
            {pending ? 'Входим…' : 'Войти'}
          </button>
        </form>
      </section>
    </main>
  )
}
