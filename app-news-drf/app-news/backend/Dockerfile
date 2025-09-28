FROM python:3.10-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    gettext \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Копирование и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание непривилегированного пользователя с определенным UID/GID
RUN groupadd -r appuser -g 1000 && useradd -r -g appuser -u 1000 appuser

# Копирование исходного кода
COPY . .

# Создание директорий для статических файлов, медиа и логов
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Изменение владельца файлов на appuser
RUN chown -R appuser:appuser /app

# Переключение на непривилегированного пользователя
USER appuser

EXPOSE 8000

# Команда по умолчанию
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]