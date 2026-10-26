import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useEffect, useMemo, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Alert } from '../../shared/ui/Alert'
import { Button } from '../../shared/ui/Button'
import { Field } from '../../shared/ui/Field'
import { Input } from '../../shared/ui/Input'
import { Textarea } from '../../shared/ui/Textarea'
import { updateMyProfile } from './api'
import { profileSchema } from './schema'
import type { UpdateProfileInput, UserProfile } from './types'

interface ProfileFormProps {
  initialData: UserProfile
}

export function ProfileForm({ initialData }: ProfileFormProps) {
  const queryClient = useQueryClient()
  const [submitMessage, setSubmitMessage] = useState<string | null>(null)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const form = useForm<UpdateProfileInput>({
    resolver: zodResolver(profileSchema),
    mode: 'onBlur',
    defaultValues: {
      company_name: initialData.company_name,
      description: initialData.description,
      contact_person: initialData.contact_person,
      phone: initialData.phone,
      address: initialData.address,
    },
  })

  useEffect(() => {
    form.reset({
      company_name: initialData.company_name,
      description: initialData.description,
      contact_person: initialData.contact_person,
      phone: initialData.phone,
      address: initialData.address,
    })
  }, [form, initialData])

  const descriptionValue = form.getValues('description') ?? ''
  const descriptionLength = useMemo(() => descriptionValue.length, [descriptionValue])

  const mutation = useMutation({
    mutationFn: updateMyProfile,
    onSuccess: (updatedProfile) => {
      queryClient.setQueryData(['profile'], updatedProfile)
      setSubmitMessage('Профиль успешно обновлён.')
      setSubmitError(null)
    },
    onError: (error: Error & { fieldErrors?: Record<string, string> }) => {
      setSubmitMessage(null)
      if (error && typeof error === 'object' && 'fieldErrors' in error) {
        Object.entries(error.fieldErrors ?? {}).forEach(([field, message]) => {
          form.setError(field as keyof UpdateProfileInput, {
            type: 'server',
            message,
          })
        })
      }
      setSubmitError(
        error instanceof Error && error.message ? error.message : 'Не удалось сохранить профиль.',
      )
    },
  })

  function handleCancel() {
    form.reset({
      company_name: initialData.company_name,
      description: initialData.description,
      contact_person: initialData.contact_person,
      phone: initialData.phone,
      address: initialData.address,
    })
    form.clearErrors()
    setSubmitMessage(null)
    setSubmitError(null)
  }

  return (
    <form className="panel-card" onSubmit={form.handleSubmit((values) => mutation.mutate(values))}>
      <div className="panel-header">
        <div>
          <h2>Редактирование профиля</h2>
        </div>
        <div className="readonly-info">
          <span>Роль: {initialData.role === 'zakazchik' ? 'Заказчик' : 'Перевозчик'}</span>
        </div>
      </div>

      <div className="form-grid">
        <Field htmlFor="company_name" label="Название компании" error={form.formState.errors.company_name?.message}>
          <Input id="company_name" {...form.register('company_name')} placeholder="ОсОО «ТендерТрак»" />
        </Field>

        <Field htmlFor="contact_person" label="Контактное лицо" error={form.formState.errors.contact_person?.message}>
          <Input id="contact_person" {...form.register('contact_person')} placeholder="Иванов Иван" />
        </Field>

        <Field htmlFor="phone" label="Телефон" error={form.formState.errors.phone?.message}>
          <Input id="phone" {...form.register('phone')} placeholder="+996XXXXXXXXX" />
        </Field>

        <Field htmlFor="address" label="Адрес" error={form.formState.errors.address?.message}>
          <Input id="address" {...form.register('address')} placeholder="г. Бишкек, ул. Ленина, 1" />
        </Field>

        <div className="read-only-grid">
          <div className="read-only-field">
            <span className="meta-label">Email</span>
            <strong>{initialData.email}</strong>
          </div>
          <div className="read-only-field">
            <span className="meta-label">ИНН</span>
            <strong>{initialData.inn}</strong>
          </div>
          <div className="read-only-field">
            <span className="meta-label">Роль</span>
            <strong>{initialData.role === 'zakazchik' ? 'Заказчик' : 'Перевозчик'}</strong>
          </div>
        </div>

        <Field htmlFor="description" label="Описание компании" error={form.formState.errors.description?.message} hint={
          <span className="char-counter">{descriptionLength}/1000</span>
        }>
          <Textarea
            id="description"
            {...form.register('description')}
            placeholder="Опишите деятельность компании и условия сотрудничества"
            maxLength={1000}
            rows={5}
          />
        </Field>
      </div>

      {(submitMessage || submitError) && (
        <div className="submit-message-wrap">
          {submitMessage ? (
            <Alert variant="success" aria-live="polite">{submitMessage}</Alert>
          ) : (
            <Alert variant="error" aria-live="assertive">{submitError}</Alert>
          )}
        </div>
      )}

      <div className="form-actions">
        <Button type="submit" variant="primary" disabled={mutation.isPending}>
          {mutation.isPending ? 'Сохранение…' : 'Сохранить'}
        </Button>
        <Button type="button" variant="quiet" onClick={handleCancel} disabled={mutation.isPending}>
          Отмена
        </Button>
      </div>
    </form>
  )
}
