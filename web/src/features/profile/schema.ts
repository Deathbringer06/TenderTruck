import { z } from 'zod'

// Mirrors UserProfileUpdate on the API: every field may be omitted or null.
export const profileUpdateSchema = z.object({
  company_name: z.string().min(2).max(120).nullable().optional(),
  description: z.string().max(1000).nullable().optional(),
  contact_person: z.string().nullable().optional(),
  phone: z.string().regex(/^\+996\d{9}$/).nullable().optional(),
  address: z.string().nullable().optional(),
})

// The profile editor keeps its current required-field experience.
export const profileSchema = z.object({
  company_name: z.string().trim().min(2, 'Введите не менее 2 символов.').max(120, 'Не более 120 символов.'),
  description: z.string().max(1000, 'Не более 1000 символов.'),
  contact_person: z.string().trim().min(1, 'Введите контактное лицо.'),
  phone: z.string().regex(/^\+996\d{9}$/, 'Введите номер в формате +996XXXXXXXXX.'),
  address: z.string().trim().min(1, 'Введите адрес.'),
})
