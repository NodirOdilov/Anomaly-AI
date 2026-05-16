# Anomaly AI — frontend

Панель аналитика на React + TypeScript + Vite + Tailwind для работы с backend.

## Быстрый старт

```bash
cd frontend
npm install
npm run dev
```

Создайте `.env` из `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Production-сборка

```bash
npm run build
npm run preview
```

## Страницы

- `/` — дашборд
- `/waf` — анализатор payload
- `/network` — анализ CSV
- `/reports` — метрики и графики
- `/docs` — встроенная документация
- `/login` — вход
- `/alerts` — поток алертов (WebSocket)
- `/admin/audit` — журнал аудита
