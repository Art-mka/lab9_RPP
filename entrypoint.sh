#!/bin/bash

# Ждем базу данных
echo "Waiting for database..."
sleep 3

# Применяем миграции
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic --noinput

# Запускаем сервер
gunicorn animal_shelter.wsgi:application --bind 0.0.0.0:8000