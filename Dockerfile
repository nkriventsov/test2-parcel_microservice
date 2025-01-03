# Используем Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости для системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry (последняя версия)
ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Настраиваем Poetry для создания окружения внутри проекта
RUN poetry config virtualenvs.in-project true
ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости проекта
RUN poetry install --with test,dev --no-root --no-interaction -vvv

# Копируем весь проект
COPY . .

