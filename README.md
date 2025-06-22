# Система управления расписанием

Веб-приложение для управления расписанием учебного заведения с возможностью создания, редактирования и экспорта расписаний.

## Возможности

- Управление группами студентов
- Управление преподавателями
- Управление предметами и кабинетами
- Создание и редактирование расписаний
- Экспорт расписаний в Excel и PDF
- Система аутентификации и авторизации
- ToDo список для пользователей

## Технологии

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **База данных**: SQLite (можно заменить на PostgreSQL/MySQL)
- **Аутентификация**: JWT токены
- **Экспорт**: openpyxl, reportlab

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd schedule-management-system
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка конфигурации

Создайте файл `.env` в корневой директории проекта:

```env
# Database Configuration
DATABASE_URL=sqlite:///./app.db

# Security (ОБЯЗАТЕЛЬНО ИЗМЕНИТЕ В ПРОДАКШЕНЕ!)
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Environment
ENVIRONMENT=production
```

### 5. Инициализация базы данных

```bash
python init_database.py
```

Этот скрипт создаст:
- Базу данных с необходимыми таблицами
- Пользователя-администратора (логин: `admin`, пароль: `admin123`)

### 6. Запуск приложения

#### Для разработки:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Для продакшена:
```bash
gunicorn -c gunicorn.conf.py app.main:app
```

### 7. Доступ к приложению

Откройте браузер и перейдите по адресу: `http://localhost:8000`

## Развертывание на хостинге

### Heroku

1. Создайте файл `Procfile`:
```
web: gunicorn -c gunicorn.conf.py app.main:app
```

2. Добавьте переменные окружения в настройках Heroku:
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
```

3. Разверните приложение:
```bash
heroku create your-app-name
git push heroku main
```

### Docker

Создайте `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]
```

### VPS/Сервер

1. Установите зависимости системы:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

2. Настройте Nginx как reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Настройте systemd сервис:
```bash
sudo nano /etc/systemd/system/schedule-app.service
```

```ini
[Unit]
Description=Schedule Management App
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
ExecStart=/path/to/your/app/venv/bin/gunicorn -c gunicorn.conf.py app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Структура проекта

```
├── app/
│   ├── api/
│   │   ├── auth.py          # Аутентификация
│   │   ├── database.py      # Настройки БД
│   │   ├── models.py        # Модели данных
│   │   ├── router.py        # API маршруты
│   │   ├── schemas.py       # Pydantic схемы
│   │   └── utils.py         # Утилиты
│   ├── static/              # Статические файлы
│   ├── templates/           # HTML шаблоны
│   └── main.py              # Точка входа
├── migrations/              # Миграции БД
├── config.py               # Конфигурация
├── requirements.txt        # Зависимости
├── gunicorn.conf.py       # Конфигурация Gunicorn
├── init_database.py       # Инициализация БД
└── README.md              # Документация
```

## API Endpoints

### Аутентификация
- `POST /api/token` - Получение JWT токена
- `POST /api/register` - Регистрация пользователя

### Пользователи
- `GET /api/users/me` - Информация о текущем пользователе
- `GET /api/users` - Список пользователей (только админ)

### Группы
- `GET /api/groups` - Список групп
- `POST /api/groups` - Создание группы
- `PUT /api/groups/{id}` - Обновление группы
- `DELETE /api/groups/{id}` - Удаление группы

### Преподаватели
- `GET /api/teachers` - Список преподавателей
- `POST /api/teachers` - Создание преподавателя
- `PUT /api/teachers/{id}` - Обновление преподавателя
- `DELETE /api/teachers/{id}` - Удаление преподавателя

### Предметы
- `GET /api/lessons` - Список предметов
- `POST /api/lessons` - Создание предмета
- `PUT /api/lessons/{id}` - Обновление предмета
- `DELETE /api/lessons/{id}` - Удаление предмета

### Кабинеты
- `GET /api/rooms` - Список кабинетов
- `POST /api/rooms` - Создание кабинета
- `PUT /api/rooms/{id}` - Обновление кабинета
- `DELETE /api/rooms/{id}` - Удаление кабинета

### Расписания
- `GET /api/schedules` - Список расписаний
- `POST /api/schedules` - Создание расписания
- `PUT /api/schedules/{id}` - Обновление расписания
- `DELETE /api/schedules/{id}` - Удаление расписания
- `GET /api/schedules/{id}/export/excel` - Экспорт в Excel
- `GET /api/schedules/{id}/export/pdf` - Экспорт в PDF

### ToDo
- `GET /api/todos` - Список задач пользователя
- `POST /api/todos` - Создание задачи
- `PUT /api/todos/{id}` - Обновление задачи
- `DELETE /api/todos/{id}` - Удаление задачи

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации.

## Поддержка

Если у вас есть вопросы или проблемы, создайте issue в репозитории.
