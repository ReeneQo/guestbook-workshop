# Официальный образ uv с уже встроенным Python 3.12.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Ставим зависимости в окружение образа, без .venv и без лишнего кэша.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

# 1) Сначала только манифесты — слой с зависимостями кешируется и не
#    пересобирается, пока не менялись pyproject.toml / uv.lock.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 2) Потом исходники — их изменение не ломает кеш зависимостей.
COPY config.py main.py ./

EXPOSE 8000

# Слушаем 0.0.0.0, иначе снаружи контейнера сервис недоступен.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
