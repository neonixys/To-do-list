# to_do_list

    Приложение для отслеживания выполнения задач

# Cтек
     Django-4.0.1, Python 3.10.7, postgres (PostgreSQL) 14.6 (Homebrew)

# Виртуальное окружение
      1. Создание окружения - python -m venv venv
      2. Активация виртуального окружения - source venv/bin/activate
      3. Выход из виртуального окружения - deactivate

# Установка зависимостей
      pip install -r requirements.txt

# .env
    poetry add envparse

# Запуск проекта
    python manage.py startapp to_do_list
    ./manage.py startapp core to_do_list/core (должен находится внутри приложения to_do_list)
    ./manage.py startapp goals to_do_list/goals

# POSTGRES
    docker images | grep postgres - postgres latest version
    docker-compose config - конфигурация

# Запуск и просмотр запущенной базы
    docker-compose up -d db - запуск
    docker-compose ps -a - просмотр


# Установка psycopg2-binary
    poetry add psycopg2-binary

# Миграции
    ./manage.py makemigrations --dry-run - что произайдет, если мы сделаем миграцию
    ./manage.py makemigrations -name 'Name of action in magration'- создаем миграции
    ./manage.py migrate - накатываем миграции

# Create Superuser
    python manage.py createsuperuser

# Runserver
    python manage.py runserver

# Docker сборка
    docker pull python:3.10.7-slim
    poetry add gunicorn - установка gunicorn
    docker-compose up -d db - запуск базы
    docker-compose down - останавливаем базу
    docker-compose up --build - сборка образа
    docker-compose up  - поднимаем образ
    python manage.py runserver - запуск сервера
    docker-compose exec api /bin/bash - вход в контейнер
    ls -la - просмотр что содержит
    docker-compose down --rmi local -v - удаляем все контейнеры и volumes

# Front
    docker-compose exec frontend /bin/sh - вход в контенер фронтп
    cd /etc/nginx/conf.d --> ls --> cat --> default.conf - просмотр файла конфигурации

# Static
    python3 manage.py collectstatic -c --no-input

# Secrets
    poetry add ansible-vault-win --group dev - формирование секретов
    ansible-vault encrypt deploy/.env - зашифровываем файл .env
    ansible-vault decrypt deploy/.env - расшифровать


# Docker
    docker-compose down --rmi local -v - удаление контейнеров и volume

# Создать пользователя в программе через терминал
    docker-compose exec api /bin/bash - проходим до файл docker-compose
    python3 manage.py createsuperuser - создаем суперпользователя

# DRF
    poetry add djangorestframework - ставим DRF
    poetry add django-extensions --group dev -     дополнения для DRF

    ./manage.py show_urls - просмотреть urls
    ./manage.py shell_plus
                >>> User.objects.last()
                <User: neonixys>
                >>> user = User.objects.last()
                 >>> user.password
# Precommit
    pre-commit run -a

# Social
    poetry add social-auth-app-django 

 # VM
    rm to_do_list_app/ -f -r

# Filters
poetry add django-filter
