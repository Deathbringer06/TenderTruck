import { http, HttpResponse } from 'msw'
import type { UpdateProfileInput, UserProfile, UserRole } from '../features/profile/types'

const defaultProfiles: Record<UserRole, UserProfile> = {
  zakazchik: {
    id: 1,
    email: 'zakazchik@example.com',
    phone: '+996555123456',
    role: 'zakazchik',
    inn: '12345678901234',
    is_verified: true,
    company_name: 'ОсОО «ТендерТрак»',
    description: 'Организация грузоперевозок по Кыргызстану и странам региона.',
    contact_person: 'Александр Иванов',
    address: 'г. Бишкек, ул. Киевская, 1',
  },
  perevozchik: {
    id: 2,
    email: 'perevozchik@example.com',
    phone: '+996700654321',
    role: 'perevozchik',
    inn: '98765432109876',
    is_verified: false,
    company_name: 'ОсОО «Быстрая доставка»',
    description: '',
    contact_person: 'Мария Петрова',
    address: 'г. Ош, ул. Ленина, 10',
  },
}

const profileStorageKey = 'tendertruck_mock_profiles'
const accountStorageKey = 'tendertruck_mock_accounts'

type MockAccount = { email: string; password: string; role: UserRole; phone: string; inn: string }

function getAccounts(): MockAccount[] {
  try {
    const stored = localStorage.getItem(accountStorageKey)
    if (stored) return JSON.parse(stored) as MockAccount[]
  } catch {
    // Ignore malformed local mock data and start with an empty account list.
  }
  return []
}

const jsonError = (detail: string, status: number) => HttpResponse.json({ detail }, { status })

function getProfiles(): Record<string, UserProfile> {
  try {
    const stored = localStorage.getItem(profileStorageKey)
    if (stored) {
      const parsed: unknown = JSON.parse(stored)
      if (typeof parsed === 'object' && parsed !== null && 'zakazchik' in parsed && 'perevozchik' in parsed) {
        return { ...defaultProfiles, ...parsed as Record<string, UserProfile> }
      }
    }
  } catch {
    // noop, then use defaults
  }

  return structuredClone(defaultProfiles)
}

let profiles = getProfiles()

function getCurrentProfile(request: Request): { role: UserRole; key: string; profile: UserProfile } | null {
  const token = request.headers.get('Authorization')?.replace(/^Bearer\s+/i, '')
  if (token === 'dev-token:zakazchik' || token === 'dev-token:perevozchik') {
    const role = token.slice('dev-token:'.length) as UserRole
    return { role, key: role, profile: profiles[role] ?? defaultProfiles[role] }
  }
  if (token?.startsWith('dev-token:')) {
    let email: string
    try {
      email = decodeURIComponent(token.slice('dev-token:'.length))
    } catch {
      return null
    }
    const account = getAccounts().find((item) => item.email === email)
    if (account) {
      const key = account.email
      const profile = profiles[key] ?? { ...defaultProfiles[account.role], email: account.email, phone: account.phone, inn: account.inn }
      return { role: account.role, key, profile }
    }
  }
  return null
}

function unauthorized() {
  return HttpResponse.json({ detail: 'Требуется авторизация.' }, { status: 401 })
}

function validate(input: unknown): Array<{ loc: string[]; msg: string; type: string }> {
  if (typeof input !== 'object' || input === null || Array.isArray(input)) {
    return [{ loc: ['body'], msg: 'Ожидался объект профиля.', type: 'value_error' }]
  }

  const body = input as UpdateProfileInput
  const errors: Array<{ loc: string[]; msg: string; type: string }> = []
  const addError = (field: keyof UpdateProfileInput, msg: string, type: string) => {
    errors.push({ loc: ['body', field], msg, type })
  }

  if (body.company_name !== undefined && body.company_name !== null) {
    if (typeof body.company_name !== 'string') addError('company_name', 'Input should be a valid string', 'string_type')
    else if (body.company_name.length < 2) addError('company_name', 'String should have at least 2 characters', 'string_too_short')
    else if (body.company_name.length > 120) addError('company_name', 'String should have at most 120 characters', 'string_too_long')
  }
  if (body.description !== undefined && body.description !== null && typeof body.description !== 'string') {
    addError('description', 'Input should be a valid string', 'string_type')
  } else if (typeof body.description === 'string' && body.description.length > 1000) {
    addError('description', 'String should have at most 1000 characters', 'string_too_long')
  }
  if (body.contact_person !== undefined && body.contact_person !== null && typeof body.contact_person !== 'string') {
    addError('contact_person', 'Input should be a valid string', 'string_type')
  } else if (typeof body.contact_person === 'string' && body.contact_person.length > 120) {
    addError('contact_person', 'String should have at most 120 characters', 'string_too_long')
  }
  if (body.phone === null) {
    addError('phone', 'Телефон нельзя очистить', 'value_error')
  } else if (body.phone !== undefined && (typeof body.phone !== 'string' || !/^\+996\d{9}$/.test(body.phone))) {
    addError('phone', 'String should match the required pattern', 'string_pattern_mismatch')
  }
  if (body.address !== undefined && body.address !== null && typeof body.address !== 'string') {
    addError('address', 'Input should be a valid string', 'string_type')
  } else if (typeof body.address === 'string' && body.address.length > 250) {
    addError('address', 'String should have at most 250 characters', 'string_too_long')
  }
  return errors
}

export const handlers = [
  http.post('/api/v1/auth/register', async ({ request }) => {
    const body = await request.json().catch(() => null) as Partial<MockAccount> | null
    if (!body || typeof body.email !== 'string' || typeof body.password !== 'string' || typeof body.phone !== 'string' || typeof body.inn !== 'string' || !body.role) {
      return jsonError('Заполните все обязательные поля.', 422)
    }
    if (body.role !== 'zakazchik' && body.role !== 'perevozchik') {
      return jsonError('Выберите допустимую роль.', 422)
    }
    const accounts = getAccounts()
    const email = body.email.trim().toLowerCase()
    const phone = body.phone.trim()
    const inn = body.inn.trim()
    if (!/^\S+@\S+\.\S+$/.test(email) || body.password.length < 8 || new TextEncoder().encode(body.password).length > 72 || phone.length > 32 || inn.length > 32) {
      return jsonError('Проверьте email, пароль, телефон и ИНН.', 422)
    }
    if (!phone || !inn || accounts.some((account) => account.email === email || account.phone === phone || account.inn === inn)) {
      return jsonError('Пользователь с такими данными уже зарегистрирован.', 400)
    }
    const account: MockAccount = { email, password: body.password, phone, inn, role: body.role }
    accounts.push(account)
    localStorage.setItem(accountStorageKey, JSON.stringify(accounts))
    const profile = { ...defaultProfiles[account.role], id: accounts.length + 2, email, phone, inn }
    profiles = { ...profiles, [email]: profile }
    localStorage.setItem(profileStorageKey, JSON.stringify(profiles))
    return HttpResponse.json(profile, { status: 201 })
  }),
  http.post('/api/v1/auth/login', async ({ request }) => {
    const body = await request.json().catch(() => null) as { email?: string; password?: string } | null
    const email = typeof body?.email === 'string' ? body.email.trim().toLowerCase() : ''
    const account = getAccounts().find((item) => item.email === email && item.password === body?.password)
    if (!account) return jsonError('Неверный email или пароль.', 401)
    return HttpResponse.json({ access_token: `dev-token:${encodeURIComponent(account.email)}`, token_type: 'bearer' })
  }),
  http.get('/api/v1/users/me', ({ request }) => {
    const current = getCurrentProfile(request)
    return current ? HttpResponse.json(current.profile) : unauthorized()
  }),
  http.put('/api/v1/users/me', async ({ request }) => {
    const current = getCurrentProfile(request)
    if (!current) return unauthorized()

    let input: unknown
    try {
      input = await request.json()
    } catch {
      return HttpResponse.json({ detail: 'Некорректный JSON.' }, { status: 422 })
    }

    const errors = validate(input)
    if (errors.length > 0) {
      return HttpResponse.json({ detail: errors }, { status: 422 })
    }

    const body = input as UpdateProfileInput
    const editableFields = ['company_name', 'description', 'contact_person', 'phone', 'address']
    const editableUpdates = Object.fromEntries(Object.entries(body).filter(([field]) => editableFields.includes(field))) as UpdateProfileInput
    if (editableUpdates.phone && getAccounts().some((account) => account.email !== current.profile.email && account.phone === editableUpdates.phone)) {
      return jsonError('Пользователь с таким телефоном уже зарегистрирован.', 400)
    }
    profiles = {
      ...profiles,
      [current.key]: { ...current.profile, ...editableUpdates },
    }
    localStorage.setItem(profileStorageKey, JSON.stringify(profiles))
    if (typeof editableUpdates.phone === 'string') {
      const accounts = getAccounts().map((account) => account.email === current.profile.email ? { ...account, phone: editableUpdates.phone! } : account)
      localStorage.setItem(accountStorageKey, JSON.stringify(accounts))
    }
    return HttpResponse.json(profiles[current.key])
  }),
]
