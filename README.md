# to_do_list

    Приложение для отслеживания выполнения задач

# Cтек
     Django-4.0.1, Python 3.10.7, postgres (PostgreSQL) 14.6 (Homebrew)

# Виртуальное окружение
      1. Создание окружения - python -m venv venv
      2. Активация виртуального окружения - source .venv/bin/activate
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
# GIT
    pre-commit run -a - прекоммит
    git switch -c dev_38 

# Social
    poetry add social-auth-app-django

 # VM
    rm to_do_list_app/ -f -r
    rm -rf to_do_list/
    
    nano .ssh/known_hosts - удалить лишнии адреса

    sudo su
    adduser deploy # создаем сложный пароль, остальные значения можем оставить по умолчанию (просто нажимаем Enter)
    usermod -aG sudo deploy # выдаем sudo права пользователю
    nano /etc/ssh/sshd_config    и   nano /etc/ssh/sshd_config.d/50-cloud-init.conf # редактируем конфигурацию, чтобы разрешить SSH по логину и паролю
    # Находим там строчку:
    # PasswordAuthentication no
    # Меняем на:
    # PasswordAuthentication yes
    # Сохраняем (:wq)
    service ssh reload # перезапускаем демон

    sudo su

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install docker-ce docker-ce-cli containerd.io
    
    # устанавливаем docker-compose
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

    # добавляем пользователя в группу Dcoker
    sudo usermod -aG docker deploy

# Filters
    poetry add django-filter

# Telegram BOT t.me/adoronin_todolist_bot
    Запрос к Telegram API - https://api.telegram.org/bot6036988019:AAHEvGh0mHA36rwXWEPIveyR-LbEpPwfvxI/getMe
    long polling для получения уведомлений - https://api.telegram.org/bot6036988019:AAHEvGh0mHA36rwXWEPIveyR-LbEpPwfvxI/getUpdates(?timeout=30)
    Отправка сообщения боту - https://api.telegram.org/bot6036988019:AAHEvGh0mHA36rwXWEPIveyR-LbEpPwfvxI/sendMessage?chat_id=632600126&text=hello

# Poetry add
    poetry add pydantic
    poetry add requests

# Shell commands
    ./manage.py  shell_plus
    from to_do_list.bot.tg.client import *
    from django.conf import settings
    settings.BOT_TOKEN
    client = TgClient(settings.BOT_TOKEN)
    client.get_updates(0, 10)
    client.get_url(Command.GET_UPDATES)
    client.send_message(632600126, 'Hello')


# Bot
    Add to config python file - runbot. Запуск скрипта manage.py с парметром runbot
    python manage.py runbot

# TESTS
    pytest . -vv - запускаем тесты
    Добавляем в конфигурацию purest - Module name: tests.tests
    faker -o faker.txt  - добавление файла faker.txt(просмотр, что может Faker)
    pytest --fixtures - просмотр fixtures

# URLS
    ./manage.py show_urls