# TenderTruck SPEC

## 1. Стек и структура
Monorepo:
- backend/app/{core,db,models,schemas,api/v1,services,ws}, backend/alembic, backend/tests
- frontend/src/{api,components/ui,components/layout,pages,hooks,store,types,lib}
- docker-compose.yml, .env.example, README.md, docs/

Backend: FastAPI, SQLAlchemy 2 async + asyncpg, Alembic, pydantic-settings, PyJWT, bcrypt, pytest (минимум).
Frontend: Vite, React 18, TS strict, Tailwind, react-router v6, TanStack Query, axios, react-hook-form + zod, zustand (только auth-store).
UI-кит свой, небольшой (Button, Input, Select, Card, Table, Badge, Modal, Tabs, Spinner, EmptyState, Toast). Светлая тема, нейтральная палитра, акцентный синий.

Docker: сервисы db (postgres:16-alpine, порт хоста 5433, т.к. на 5432 уже стоит локальный Postgres), backend (uvicorn --reload, порт 8000), frontend (vite dev, порт 5173). Конфиг через .env, образец в .env.example. Swagger на /docs.

## 2. Роли
- admin
- customer (Заказчик) и carrier (Перевозчик). Роль выбирается при регистрации.
- Внутри компании сотрудник: owner, logist, dispatcher, accountant (CompanyMember.position). Права: owner всё; logist создаёт/ведёт тендеры/рейсы; dispatcher назначает водителей и машины; accountant только просмотр документов и рейсов.

## 3. Модели БД
User(id, email unique nullable, phone unique nullable, password_hash, role, is_active, is_blocked, created_at)
Company(id, name, inn, legal_address, contact_phone, contact_email, description, verification_status[pending|verified|rejected], owner_id)
CompanyMember(id, company_id, user_id, position, full_name)
Vehicle(id, company_id, plate, kind[tractor|trailer|truck], body_type_id, capacity_kg, volume_m3, is_active)
Driver(id, company_id, full_name, phone, license_no)
BodyType(id, name), CargoType(id, name), Currency(id, code, name), Geozone(id, name, kind[region|city])
Tender(id, customer_company_id, created_by, title, status, type[open|closed], origin_text, destination_text, origin_geozone_id, destination_geozone_id, cargo_type_id, weight_kg, volume_m3, body_type_id, temperature_mode, adr_class, loading_at, unloading_at, start_price, bid_step, currency_id, starts_at, ends_at, winner_bid_id nullable, created_at)
TenderInvite(tender_id, carrier_company_id)  # для закрытых
Bid(id, tender_id, carrier_company_id, price, is_auto, created_at)
AutoBid(id, tender_id, carrier_company_id, min_price, is_active)  # unique(tender_id, carrier_company_id)
Trip(id, tender_id unique, carrier_company_id, driver_id nullable, tractor_id nullable, trailer_id nullable, status, created_at) + TripStatusLog(trip_id, status, at)
Notification(id, user_id, kind, title, body, is_read, created_at)

Статусы Tender: draft, active, closed (время вышло, ждёт выбора), awarded, cancelled.
Статусы Trip: waiting_loading -> in_transit -> arrived -> completed.
Индексы на внешние ключи и (status, ends_at).

## 4. Auth (backend + frontend)
- Регистрация по email+пароль или phone+пароль, выбор роли, ИНН, название компании. Подтверждение телефона по SMS-коду: SMS-провайдер замоканный, в dev код пишется в лог и всегда принимается 123456.
- Логин по логину/паролю или телефон+SMS. JWT access (15 мин) + refresh (7 дней), refresh хранить в БД и ротировать. Восстановление пароля по тому же mock-коду.
- Валидация ИНН: 14 цифр (КР), правило вынести в одну функцию. Реальный скоринг НЕ делать, только интерфейс-заглушка services/scoring.py (возвращает "unknown").
- Зависимости get_current_user, require_role(...). Заблокированный пользователь получает 403.
- 2FA не делать, оставить TODO в DECISIONS.md.

## 5. Тендеры и ставки
Заказчик: создаёт тендер (форма из полей Tender, шаги: маршрут -> груз -> условия торга), сохраняет черновиком, публикует (draft -> active), отменяет, продлевает ends_at. Открытый тендер видят все верифицированные перевозчики, закрытый только приглашённые.
Перевозчик: список активных тендеров с фильтрами (регион, тип кузова, даты), страница тендера, подача ставки.
Правила ставки (в одной транзакции, SELECT ... FOR UPDATE на tender):
- тендер active и now < ends_at;
- price <= start_price и price <= (текущий минимум - bid_step), для первой ставки price <= start_price;
- участник видит чужие цены как "Участник №N" (N стабильный номер в рамках тендера), заказчик видит названия компаний только после awarded.
Авто-брокер: AutoBid(min_price). После каждой новой ставки для каждого активного AutoBid других перевозчиков, где min_price <= текущий минимум - bid_step, ставится ставка max(min_price, минимум - bid_step) с is_auto=true. Цикл с ограничением итераций (защита от бесконечности), в services/auto_broker.py.
Закрытие: фоновая задача раз в 5 сек переводит active -> closed при now >= ends_at. Заказчик вручную выбирает победителя (любую ставку, обычно минимальную) -> tender.awarded, winner_bid_id, создаётся Trip(waiting_loading).
Real-time: WebSocket /ws/tenders/{id} (события bid_placed, tender_closed, tender_awarded), /ws/notifications. Простой in-process ConnectionManager, авторизация токеном в query. Redis НЕ использовать.

## 6. Рейсы (минимум)
Перевозчик ведёт статусы Trip по цепочке, каждая смена пишется в TripStatusLog и шлёт Notification заказчику. Страница рейса показывает таймлайн статусов.
Назначение водителя/тягача/прицепа: ТОЛЬКО поле в модели и пустая заглушка формы "Скоро" (делает человек).

## 7. Админка
Список компаний с фильтром по verification_status, кнопки верифицировать/отклонить; список пользователей, блокировка/разблокировка; CRUD справочников BodyType, CargoType, Currency, Geozone; список всех тендеров только на чтение. Арбитраж: вкладка-заглушка.

## 8. Интерфейс
Layout: sidebar слева (вкладки по роли), topbar с колокольчиком уведомлений и меню профиля. Защита маршрутов по роли, редирект на /login. Страницы 404/403.
Customer: Дашборд, Мои тендеры, Создать тендер, Рейсы, Документы (заглушка), Компания (реквизиты, сотрудники).
Carrier: Дашборд, Поиск тендеров, Мои ставки, Рейсы, Автопарк (машины), Водители, Документы (заглушка), Компания.
Admin: Дашборд, Компании, Пользователи, Тендеры, Справочники, Арбитраж (заглушка).
Дашборд: только карточки KPI (счётчики из одного эндпоинта /api/v1/dashboard/summary по роли) и таблица последних 5 событий. Графики НЕ делать (заглушка-блок "Аналитика скоро").
Везде: загрузка (skeleton/spinner), пустые состояния, ошибки через Toast, адаптив до 375px.

## 9. НЕ делать (оставить человеку)
PDF-документы и ЭЦП/ТТН, загрузка сканов и фото, отзывы и оценки, графики и аналитические отчёты, чат рейса, реальный скоринг по ИНН, Telegram/Push, 2FA, GPS-трекинг, REST-интеграции с 1С/SAP.
Для каждого пункта оставь пустой роутер/страницу-заглушку с понятным именем файла, чтобы человек мог подключиться.

## 10. Seed и качество
scripts/seed.py: admin@tendertruck.kg / Admin123!, demo-заказчик, demo-перевозчик (верифицированные), справочники (около 10 типов кузова, около 15 типов грузов, KGS/USD/RUB/KZT/EUR, регионы КР и крупные города), 3 демо-тендера.
Тесты: только pytest на правила ставки и авто-брокер (5-8 тестов).