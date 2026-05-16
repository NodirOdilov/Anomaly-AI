# Аутентификация и авторизация

> Модель безопасности Anomaly AI v2: JWT, API-ключи, RBAC.

| Параметр | Значение |
|----------|----------|
| Роли | `viewer`, `analyst`, `admin` |
| Dev по умолчанию | `AUTH_REQUIRED=false` |
| Репозиторий | [NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI) |

## Содержание

1. [Обзор](#обзор)
2. [Конфигурация](#конфигурация)
3. [Хэширование паролей](#хэширование-паролей)
4. [Эндпоинты](#эндпоинты)
5. [API-ключи](#api-ключи)
6. [Безопасные значения по умолчанию](#безопасные-значения-по-умолчанию)

---

## Обзор

Anomaly AI поддерживает **два** способа аутентификации:

1. **JWT** — короткоживущие access-токены (15 минут) + долгоживущие refresh (7 дней).
   Используется UI-консолью.
2. **API-ключи** — для машинных интеграций (CI/CD, SIEM-плагины, скрипты).
   Формат: `aa_live_<32_random>`.

Поверх — **RBAC** с тремя ролями:

| Роль       | Уровень | Может |
|------------|---------|-------|
| `viewer`   | 1       | Читать дашборд, отчёты, делать predict |
| `analyst`  | 2       | Всё что viewer + просмотр audit/alerts |
| `admin`    | 3       | Всё + управление пользователями, моделями, SIEM |

## Конфигурация

```bash
AUTH_REQUIRED=true               # включить аутентификацию (по умолчанию false в dev)
JWT_SECRET=<openssl rand -base64 64>
JWT_ALGORITHM=HS256
JWT_ACCESS_TTL_MINUTES=15
JWT_REFRESH_TTL_DAYS=7
BOOTSTRAP_ADMIN_EMAIL=admin@example.com
BOOTSTRAP_ADMIN_PASSWORD=<strong_password>
```

При первом старте, если БД пуста, автоматически создаётся учётка из
`BOOTSTRAP_ADMIN_*`. Сразу после первого логина **обязательно смените пароль**.

## Хэширование паролей

Используется **Argon2id** (через `passlib[argon2]`) — современный OWASP-рекомендованный
алгоритм. Параметры:

- `memory_cost=65536` (64 MiB)
- `time_cost=3`
- `parallelism=4`

## Эндпоинты

### Вход (login)

```http
POST /api/v1/auth/login
Content-Type: application/json

{ "email": "user@example.com", "password": "..." }
```

Ответ:

```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "Bearer",
  "access_expires_in": 900,
  "refresh_expires_in": 604800
}
```

### Обновление токена (refresh)

```http
POST /api/v1/auth/refresh
{ "refresh_token": "..." }
```

### Выход (logout, отзыв refresh)

```http
POST /api/v1/auth/logout
{ "refresh_token": "..." }
```

### Профиль

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

## API-ключи

### Создание

```http
POST /api/v1/auth/api-keys
Authorization: Bearer <jwt>

{ "name": "splunk-export", "scopes": "predict" }
```

Ответ содержит поле `plain` — **полный ключ показывается ОДИН раз**:

```json
{
  "id": 1,
  "name": "splunk-export",
  "prefix": "aa_live_a1b2c3",
  "plain": "aa_live_a1b2c3d4e5f6...",
  "created_at": "2026-05-16T10:00:00Z",
  "expires_at": null,
  "scopes": "predict"
}
```

### Использование

```http
POST /api/v1/waf/predict
X-API-Key: aa_live_a1b2c3d4e5f6...

{ "payload": "id=1' OR '1'='1" }
```

### Отзыв

```http
DELETE /api/v1/auth/api-keys/{id}
```

## Безопасные значения по умолчанию

- В `production` (`APP_ENV=production`) при пустом `JWT_SECRET` приложение
  сгенерирует случайный 64-байтный секрет — но при рестарте он изменится
  и все токены инвалидируются. **Всегда** задавайте `JWT_SECRET` явно в проде.
- Cookies не используются — только заголовки. Это позволяет работать кросс-доменно
  без CSRF, но требует от клиента самостоятельного хранения refresh-токена.
- WebSocket принимает JWT в query-параметре `?token=...` (стандарт ограничения
  WebSocket-клиентов). Используйте `wss://` для шифрования.

## См. также

- [`MONITORING.md`](MONITORING.md) — метрика `anomaly_ai_auth_logins_total`
- [`SECURITY.md`](../SECURITY.md) — политика безопасности
- [`API.md`](API.md) — эндпоинты auth
