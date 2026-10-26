export type UserRole = 'zakazchik' | 'perevozchik'

export interface UserProfile {
  id: number
  email: string
  phone: string
  role: UserRole
  inn: string
  is_verified: boolean
  company_name: string | null
  description: string | null
  contact_person: string | null
  address: string | null
}

export interface UpdateProfileInput {
  company_name?: string | null
  description?: string | null
  contact_person?: string | null
  phone?: string
  address?: string | null
}
