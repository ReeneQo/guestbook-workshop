# 📒 guestbook

Небольшая **гостевая книга** на FastAPI: можно оставить сообщение и посмотреть все оставленные. Данные хранятся в PostgreSQL.

## Что умеет

- `GET /` — приветствие
- `GET /health` — проверка «жив ли сервис»
- `GET /messages` — список сообщений (новые сверху)
- `POST /messages` — добавить сообщение: тело `{"author": "...", "text": "..."}`

## Как это устроено

- Зависимости зафиксированы через **uv**: `pyproject.toml` + `uv.lock`, версия Python — в `.python-version`.
- Конфигурация — в `config.py` на **pydantic-settings**: в коде нет зашитых адресов и паролей.
- Секреты живут в `.env` (он в `.gitignore`); в репозитории — только шаблон `.env.example`.
- Контейнеризация: `Dockerfile` + `.dockerignore`, оркестрация — `compose.yaml` (app + PostgreSQL).

## 🚀 Запуск через Docker Compose (рекомендуется)

```bash
cp .env.example .env     # заполните POSTGRES_PASSWORD своим значением
docker compose up -d     # поднимет app + db одной командой
```

Сервис будет доступен на <http://localhost:8000>. Наружу проброшен только `app`;
база доступна лишь приложению внутри сети Compose. Данные хранятся в volume `pgdata`
и переживают `docker compose down` / `up` (том удаляется только с `down -v`).

Проверка:

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/messages \
  -H 'Content-Type: application/json' \
  -d '{"author": "Ада", "text": "Первое сообщение"}'
curl http://localhost:8000/messages
```

## 🧪 Локальный запуск без Docker

Нужен работающий PostgreSQL. Параметры подключения — в `.env`
(для локального запуска `POSTGRES_HOST=localhost`).

```bash
uv sync                               # поставит зависимости в .venv по uv.lock
uv run uvicorn main:app --reload      # http://localhost:8000
```

## 📁 Структура

| Файл             | Назначение                                             |
| ---------------- | ------------------------------------------------------ |
| `main.py`        | FastAPI-приложение и эндпоинты                          |
| `config.py`      | настройки на pydantic-settings (единая точка конфига)   |
| `pyproject.toml` | зависимости и метаданные проекта (uv)                   |
| `uv.lock`        | точные версии зависимостей                              |
| `Dockerfile`     | сборка образа приложения                                |
| `compose.yaml`   | оркестрация app + PostgreSQL                            |
| `.env.example`   | шаблон переменных окружения                             |
