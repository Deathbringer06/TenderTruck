# TenderTruck Web

React + TypeScript интерфейс TenderTruck.

## Разработка

Из каталога `web` запустите `npm ci`, затем `npm run dev`. Vite проксирует запросы `/api` на backend по адресу `http://localhost:8000`. Для изолированной разработки задайте `VITE_USE_MOCKS=true` в локальном `.env`.

## Production

`npm run build` собирает приложение в `dist`. Docker Compose собирает этот каталог в Nginx-образ и проксирует `/api/` в FastAPI.
