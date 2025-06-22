# Руководство по развертыванию

## 1. Подготовка к GitHub

### Шаг 1: Инициализация Git репозитория
```bash
git init
git add .
git commit -m "Initial commit"
```

### Шаг 2: Создание репозитория на GitHub
1. Перейдите на [GitHub](https://github.com)
2. Нажмите "New repository"
3. Введите название репозитория
4. НЕ ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license"
5. Нажмите "Create repository"

### Шаг 3: Подключение локального репозитория к GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## 2. Развертывание на Heroku

### Шаг 1: Установка Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Шаг 2: Вход в Heroku
```bash
heroku login
```

### Шаг 3: Создание приложения на Heroku
```bash
heroku create your-app-name
```

### Шаг 4: Настройка переменных окружения
```bash
heroku config:set SECRET_KEY="your-super-secret-key-change-this"
heroku config:set ALGORITHM="HS256"
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES="30"
heroku config:set ENVIRONMENT="production"
```

### Шаг 5: Добавление базы данных PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### Шаг 6: Деплой приложения
```bash
git push heroku main
```

### Шаг 7: Инициализация базы данных
```bash
heroku run python init_database.py
```

### Шаг 8: Открытие приложения
```bash
heroku open
```

## 3. Развертывание на Railway

### Шаг 1: Подключение к Railway
1. Перейдите на [Railway](https://railway.app)
2. Войдите через GitHub
3. Нажмите "New Project"
4. Выберите "Deploy from GitHub repo"

### Шаг 2: Настройка переменных окружения
В настройках проекта добавьте:
```
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
```

### Шаг 3: Настройка базы данных
1. Добавьте PostgreSQL сервис
2. Скопируйте DATABASE_URL в переменные окружения

## 4. Развертывание на Render

### Шаг 1: Создание сервиса
1. Перейдите на [Render](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите GitHub репозиторий

### Шаг 2: Настройка
- **Name**: your-app-name
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -c gunicorn.conf.py app.main:app`

### Шаг 3: Переменные окружения
Добавьте все необходимые переменные в Environment Variables.

## 5. Развертывание на VPS (Ubuntu/Debian)

### Шаг 1: Подготовка сервера
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx git
```

### Шаг 2: Клонирование репозитория
```bash
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
sudo chown -R $USER:$USER YOUR_REPO_NAME
cd YOUR_REPO_NAME
```

### Шаг 3: Настройка виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Шаг 4: Создание файла .env
```bash
nano .env
```
Добавьте:
```env
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=sqlite:///./app.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
HOST=127.0.0.1
PORT=8000
DEBUG=False
```

### Шаг 5: Инициализация базы данных
```bash
python init_database.py
```

### Шаг 6: Настройка systemd сервиса
```bash
sudo nano /etc/systemd/system/schedule-app.service
```

Добавьте:
```ini
[Unit]
Description=Schedule Management App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/YOUR_REPO_NAME
Environment=PATH=/var/www/YOUR_REPO_NAME/venv/bin
ExecStart=/var/www/YOUR_REPO_NAME/venv/bin/gunicorn -c gunicorn.conf.py app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Шаг 7: Запуск сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable schedule-app
sudo systemctl start schedule-app
```

### Шаг 8: Настройка Nginx
```bash
sudo nano /etc/nginx/sites-available/schedule-app
```

Добавьте:
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
        alias /var/www/YOUR_REPO_NAME/app/static/;
    }
}
```

### Шаг 9: Активация сайта
```bash
sudo ln -s /etc/nginx/sites-available/schedule-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Настройка домена и SSL

### Шаг 1: Настройка DNS
Укажите A-запись вашего домена на IP-адрес сервера.

### Шаг 2: Установка Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### Шаг 3: Получение SSL сертификата
```bash
sudo certbot --nginx -d your-domain.com
```

## 7. Мониторинг и логи

### Просмотр логов приложения
```bash
sudo journalctl -u schedule-app -f
```

### Просмотр логов Nginx
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 8. Обновление приложения

### Автоматическое обновление через GitHub Actions
При каждом push в main ветку приложение будет автоматически обновляться.

### Ручное обновление на VPS
```bash
cd /var/www/YOUR_REPO_NAME
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart schedule-app
```

## 9. Резервное копирование

### Создание бэкапа базы данных
```bash
cp /var/www/YOUR_REPO_NAME/app.db /backup/app_$(date +%Y%m%d_%H%M%S).db
```

### Автоматическое резервное копирование
Создайте cron задачу:
```bash
crontab -e
```

Добавьте:
```cron
0 2 * * * cp /var/www/YOUR_REPO_NAME/app.db /backup/app_$(date +\%Y\%m\%d_\%H\%M\%S).db
``` 