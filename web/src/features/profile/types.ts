export type UserRole = 'zakazchik' | 'perevozchik'

export interface UserProfile {
  id: number
  email: string
  phone: string
  role: UserRole
  inn: string
  is_verified: boolean
  company_name: string
  description: string
  contact_person: string
  address: string
}

export interface UpdateProfileInput {
  company_name: string
  description: string
  contact_person: string
  phone: string
  address: string
}
