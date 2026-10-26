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

function getProfiles(): Record<UserRole, UserProfile> {
  try {
    const stored = localStorage.getItem(profileStorageKey)
    if (stored) {
      const parsed: unknown = JSON.parse(stored)
      if (typeof parsed === 'object' && parsed !== null && 'zakazchik' in parsed && 'perevozchik' in parsed) {
        return parsed as Record<UserRole, UserProfile>
      }
    }
  } catch {
    // noop, then use defaults
  }

  return structuredClone(defaultProfiles)
}

let profiles = getProfiles()

function getRole(request: Request): UserRole | null {
  const token = request.headers.get('Authorization')?.replace(/^Bearer\s+/i, '')
  if (token === 'dev-token:zakazchik') return 'zakazchik'
  if (token === 'dev-token:perevozchik') return 'perevozchik'
  return null
}

function unauthorized() {
  return HttpResponse.json({ detail: 'Требуется авторизация.' }, { status: 401 })
}

function validate(input: unknown): Array<{ loc: string[]; msg: string; type: string }> {
  if (typeof input !== 'object' || input === null) {
    return [{ loc: ['body'], msg: 'Ожидался объект профиля.', type: 'value_error' }]
  }

  const body = input as UpdateProfileInput
  const errors: Array<{ loc: string[]; msg: string; type: string }> = []
  const addError = (field: keyof UpdateProfileInput, msg: string, type: string) => {
    errors.push({ loc: ['body', field], msg, type })
  }

  if (body.company_name !== undefined && body.company_name !== null && body.company_name.length < 2) {
    addError('company_name', 'String should have at least 2 characters', 'string_too_short')
  } else if (typeof body.company_name === 'string' && body.company_name.length > 120) {
    addError('company_name', 'String should have at most 120 characters', 'string_too_long')
  }
  if (body.description !== undefined && body.description !== null && typeof body.description !== 'string') {
    addError('description', 'Input should be a valid string', 'string_type')
  } else if (typeof body.description === 'string' && body.description.length > 1000) {
    addError('description', 'String should have at most 1000 characters', 'string_too_long')
  }
  if (body.contact_person !== undefined && body.contact_person !== null && typeof body.contact_person !== 'string') {
    addError('contact_person', 'Input should be a valid string', 'string_type')
  }
  if (body.phone !== undefined && body.phone !== null && (typeof body.phone !== 'string' || !/^\+996\d{9}$/.test(body.phone))) {
    addError('phone', 'String should match pattern '^\\+996\\d{9}$'', 'string_pattern_mismatch')
  }
  if (body.address !== undefined && body.address !== null && typeof body.address !== 'string') {
    addError('address', 'Input should be a valid string', 'string_type')
  }
  return errors
}

export const handlers = [
  http.get('/api/v1/users/me', ({ request }) => {
    const role = getRole(request)
    return role ? HttpResponse.json(profiles[role]) : unauthorized()
  }),
  http.put('/api/v1/users/me', async ({ request }) => {
    const role = getRole(request)
    if (!role) return unauthorized()

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
    profiles = {
      ...profiles,
      [role]: { ...profiles[role], ...body },
    }
    localStorage.setItem(profileStorageKey, JSON.stringify(profiles))
    return HttpResponse.json(profiles[role])
  }),
]
