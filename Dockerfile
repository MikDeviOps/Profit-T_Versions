FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов проекта
COPY . .

# Установка Python зависимостей
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir \
    aiogram==3.1.1 \
    python-dotenv

# Создание директории для файлов истории
RUN mkdir -p /data/history_files
ENV LOG_FOLDER=/data/history_files

CMD ["python", "main.py"]