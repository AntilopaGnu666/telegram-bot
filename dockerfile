# Базовый образ
FROM python:3.10-slim

# Рабочая директория
WORKDIR ~/telegram-bot

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y \
        gcc \
        libpq-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода бота
COPY . .

# Команда запуска
CMD ["python", "main.py"]






