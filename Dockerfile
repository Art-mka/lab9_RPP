# Dockerfile для Python 3.14.4
# Используем nightly build или development образ
FROM python:3.14-rc-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE animal_shelter.settings

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip для Python 3.14
RUN pip install --upgrade pip setuptools wheel

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Собираем статические файлы (синтаксис Django 6.0)
RUN python manage.py collectstatic --noinput --clear

# Запуск с Gunicorn для Django 6.0
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "animal_shelter.wsgi:application"]