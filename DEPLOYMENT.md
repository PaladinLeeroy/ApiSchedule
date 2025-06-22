# Инструкции по развертыванию

## Быстрый старт

Для быстрого развертывания выполните:

```bash
python deploy.py
```

Этот скрипт автоматически:
- Проверит версию Python
- Создаст файл .env
- Установит зависимости
- Инициализирует базу данных
- Проверит готовность к запуску

## Развертывание на различных платформах

### 1. Локальный сервер / VPS

#### Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv nginx git

# Создание пользователя для приложения
sudo useradd -m -s /bin/bash appuser
sudo usermod -aG sudo appuser
```

#### Развертывание приложения

```bash
# Переключение на пользователя приложения
sudo su - appuser

# Клонирование репозитория
git clone <your-repo-url> schedule-app
cd schedule-app

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp env.example .env
nano .env  # Измените SECRET_KEY и другие настройки

# Инициализация базы данных
python init_database.py
```

#### Настройка Nginx

```bash
sudo nano /etc/nginx/sites-available/schedule-app
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/appuser/schedule-app/app/static/;
        expires 30d;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/schedule-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Настройка systemd сервиса

```bash
sudo nano /etc/systemd/system/schedule-app.service
```

```ini
[Unit]
Description=Schedule Management App
After=network.target

[Service]
User=appuser
Group=appuser
WorkingDirectory=/home/appuser/schedule-app
Environment=PATH=/home/appuser/schedule-app/venv/bin
ExecStart=/home/appuser/schedule-app/venv/bin/gunicorn -c gunicorn.conf.py app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable schedule-app
sudo systemctl start schedule-app
```

### 2. Heroku

#### Подготовка

1. Установите Heroku CLI
2. Войдите в аккаунт: `heroku login`

#### Развертывание

```bash
# Создание приложения
heroku create your-app-name

# Добавление PostgreSQL
heroku addons:create heroku-postgresql:mini

# Настройка переменных окружения
heroku config:set SECRET_KEY="your-super-secret-key"
heroku config:set ALGORITHM="HS256"
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES="30"
heroku config:set ENVIRONMENT="production"

# Развертывание
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Запуск миграций
heroku run python init_database.py
```

### 3. Railway

#### Подготовка

1. Создайте аккаунт на Railway.app
2. Подключите GitHub репозиторий

#### Настройка

1. В настройках проекта добавьте переменные окружения:
   - `SECRET_KEY`
   - `ALGORITHM`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`
   - `ENVIRONMENT`

2. Railway автоматически определит команду запуска из `Procfile`

### 4. DigitalOcean App Platform

#### Подготовка

1. Создайте аккаунт на DigitalOcean
2. Перейдите в App Platform

#### Настройка

1. Подключите GitHub репозиторий
2. Выберите Python как runtime
3. Укажите команду запуска: `gunicorn -c gunicorn.conf.py app.main:app`
4. Добавьте переменные окружения
5. Настройте базу данных (PostgreSQL)

### 5. Docker

#### Локальный запуск

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

#### Продакшен с Docker

```bash
# Сборка образа
docker build -t schedule-app .

# Запуск контейнера
docker run -d \
  --name schedule-app \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="postgresql://..." \
  schedule-app
```

### 6. Google Cloud Run

#### Подготовка

1. Установите Google Cloud SDK
2. Настройте проект: `gcloud config set project YOUR_PROJECT_ID`

#### Развертывание

```bash
# Сборка и развертывание
gcloud run deploy schedule-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY="your-secret-key"
```

## Настройка базы данных

### SQLite (разработка)

```env
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL (продакшен)

```env
DATABASE_URL=postgresql://username:password@host:port/database
```

### MySQL (продакшен)

Добавьте в `requirements.txt`:
```
mysqlclient
```

```env
DATABASE_URL=mysql://username:password@host:port/database
```

## Безопасность

### Обязательные меры

1. **Измените SECRET_KEY**:
   ```bash
   # Генерация безопасного ключа
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Настройте HTTPS**:
   - Используйте Let's Encrypt для бесплатных сертификатов
   - Настройте редирект с HTTP на HTTPS

3. **Настройте CORS**:
   ```python
   # В main.py измените CORS настройки
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-domain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Измените пароль администратора**:
   - Войдите в систему
   - Перейдите в настройки профиля
   - Измените пароль

### Дополнительные меры

1. **Настройте файрвол**:
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

2. **Настройте мониторинг**:
   ```bash
   # Установка мониторинга
   sudo apt install htop iotop
   ```

3. **Настройте резервное копирование**:
   ```bash
   # Скрипт для бэкапа
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   cp app.db backup/app.db.$DATE
   ```

## Мониторинг и логи

### Просмотр логов

```bash
# systemd сервис
sudo journalctl -u schedule-app -f

# Docker
docker-compose logs -f

# Heroku
heroku logs --tail
```

### Мониторинг производительности

```bash
# Проверка использования ресурсов
htop
df -h
free -h
```

## Обновление приложения

### Локальный сервер

```bash
cd /path/to/app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python init_database.py
sudo systemctl restart schedule-app
```

### Docker

```bash
docker-compose pull
docker-compose up -d
```

### Heroku

```bash
git push heroku main
heroku run python init_database.py
```

## Устранение неполадок

### Частые проблемы

1. **Порт занят**:
   ```bash
   sudo netstat -tulpn | grep :8000
   sudo kill -9 PID
   ```

2. **Проблемы с правами**:
   ```bash
   sudo chown -R appuser:appuser /path/to/app
   ```

3. **Проблемы с базой данных**:
   ```bash
   python init_database.py
   ```

4. **Проблемы с зависимостями**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Получение помощи

1. Проверьте логи приложения
2. Проверьте логи Nginx: `sudo tail -f /var/log/nginx/error.log`
3. Проверьте статус сервиса: `sudo systemctl status schedule-app` 