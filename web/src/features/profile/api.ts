import { apiRequest } from '../../shared/api/client'
import type { UpdateProfileInput, UserProfile } from './types'

export function getMyProfile() {
  return apiRequest<UserProfile>('/users/me')
}

export function updateMyProfile(input: UpdateProfileInput) {
  return apiRequest<UserProfile>('/users/me', {
    method: 'PUT',
    body: JSON.stringify(input),
  })
}
