import { useQuery } from '@tanstack/react-query'
import { Alert } from '../../shared/ui/Alert'
import { getMyProfile } from './api'
import { ProfileForm } from './ProfileForm'

const roleLabels = {
  zakazchik: 'Заказчик',
  perevozchik: 'Перевозчик',
} as const

export function ProfilePage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['profile'],
    queryFn: getMyProfile,
  })

  if (isLoading) {
    return (
      <section className="page-shell">
        <div className="state-card">
          <p>Загрузка данных профиля…</p>
        </div>
      </section>
    )
  }

  if (isError) {
    return (
      <section className="page-shell">
        <Alert variant="error" className="state-card">
          {error instanceof Error ? error.message : 'Не удалось загрузить профиль.'}
        </Alert>
      </section>
    )
  }

  if (!data) {
    return (
      <section className="page-shell">
        <Alert variant="info" className="state-card">
          Профиль пока пустой.
        </Alert>
      </section>
    )
  }

  const roleName = roleLabels[data.role]

  return (
    <section className="page-shell">
      <div className="page-heading">
        <span className="eyebrow">ЛИЧНЫЙ КАБИНЕТ</span>
        <h1>Мой профиль</h1>
      </div>

      <div className="profile-card">
        <div className="profile-header-row">
          <div>
            <p className="profile-company-name">{data.company_name || 'Компания не указана'}</p>
            <div className="inline-badges">
              <span className="role-badge">{roleName}</span>
              <span className={`status-badge ${data.is_verified ? 'verified' : 'pending'}`}>
                {data.is_verified ? 'Верифицирован' : 'Ожидает верификации'}
              </span>
            </div>
          </div>
        </div>

        <div className="profile-grid">
          <div className="meta-item">
            <span className="meta-label">ИНН</span>
            <strong>{data.inn}</strong>
          </div>
          <div className="meta-item">
            <span className="meta-label">Email</span>
            <strong>{data.email}</strong>
          </div>
          <div className="meta-item">
            <span className="meta-label">Телефон</span>
            <strong>{data.phone}</strong>
          </div>
          <div className="meta-item">
            <span className="meta-label">Контактное лицо</span>
            <strong>{data.contact_person}</strong>
          </div>
          <div className="meta-item full-width">
            <span className="meta-label">Адрес</span>
            <strong>{data.address}</strong>
          </div>
        </div>

        <div className="description-block">
          <h2>О компании</h2>
          <p>{data.description || 'Описание компании не добавлено.'}</p>
        </div>
      </div>

      <ProfileForm initialData={data} />
    </section>
  )
}
