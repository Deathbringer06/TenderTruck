import { useState, type FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ApiError, apiRequest } from '../shared/api/client'

type AuthMode = 'login' | 'register'
type AuthResponse = { access_token: string; token_type: string }

export function AuthPage() {
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [inn, setInn] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<'zakazchik' | 'perevozchik'>('zakazchik')
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const mode: AuthMode = location.pathname === '/register' ? 'register' : 'login'

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setPending(true)
    try {
      if (mode === 'register') {
        await apiRequest('/auth/register', {
          method: 'POST',
          body: JSON.stringify({ email, phone, inn, password, role }),
        })
      }
      const token = await apiRequest<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      localStorage.setItem('access_token', token.access_token)
      window.dispatchEvent(new Event('auth:changed'))
      navigate((location.state as { from?: string } | null)?.from ?? '/cabinet/profile', { replace: true })
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : 'Не удалось выполнить запрос. Проверьте соединение с сервером.')
    } finally {
      setPending(false)
    }
  }

  return (
    <main className="login-screen">
      <section className="login-card" aria-labelledby="auth-title">
        <span className="eyebrow">ТендерТрак</span>
        <h1 id="auth-title">{mode === 'login' ? 'Вход в кабинет' : 'Регистрация компании'}</h1>
        <p className="muted-copy">{mode === 'login' ? 'Войдите, чтобы продолжить работу.' : 'Создайте аккаунт заказчика или перевозчика.'}</p>
        <form className="login-actions" onSubmit={handleSubmit}>
          {mode === 'register' && <>
            <label className="field"><span className="field-label">Роль</span>
              <select className="text-input" value={role} onChange={(event) => setRole(event.target.value as typeof role)}>
                <option value="zakazchik">Заказчик</option><option value="perevozchik">Перевозчик</option>
              </select>
            </label>
            <label className="field"><span className="field-label">Телефон</span><input className="text-input" type="tel" autoComplete="tel" required value={phone} onChange={(event) => setPhone(event.target.value)} /></label>
            <label className="field"><span className="field-label">ИНН</span><input className="text-input" required value={inn} onChange={(event) => setInn(event.target.value)} /></label>
          </>}
          <label className="field"><span className="field-label">Email</span><input className="text-input" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} /></label>
          <label className="field"><span className="field-label">Пароль</span><input className="text-input" type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'} minLength={8} required value={password} onChange={(event) => setPassword(event.target.value)} /></label>
          {error && <p className="field-error" role="alert">{error}</p>}
          <button className="button button-primary" type="submit" disabled={pending}>{pending ? 'Подождите…' : mode === 'login' ? 'Войти' : 'Зарегистрироваться'}</button>
        </form>
        <p className="auth-switch">
          {mode === 'login' ? <>Нет аккаунта? <Link to="/register">Зарегистрироваться</Link></> : <>Уже зарегистрированы? <Link to="/login">Войти</Link></>}
        </p>
      </section>
    </main>
  )
}
