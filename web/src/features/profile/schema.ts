import { z } from 'zod'

export const profileSchema = z.object({
  company_name: z.string().trim().min(2, 'Введите не менее 2 символов.').max(120, 'Не более 120 символов.'),
  description: z.string().max(1000, 'Не более 1000 символов.'),
  contact_person: z.string().trim().min(1, 'Введите контактное лицо.'),
  phone: z.string().regex(/^\+996\d{9}$/, 'Введите номер в формате +996XXXXXXXXX.'),
  address: z.string().trim().min(1, 'Введите адрес.'),
})
