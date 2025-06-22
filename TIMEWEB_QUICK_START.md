# 🚀 Быстрый деплой на Timeweb Cloud Apps

## Настройка в Timeweb Cloud Apps

### 1. Основные настройки
- **Источник**: GitHub
- **Репозиторий**: `PaladinLeeroy/ApiSchedule`
- **Ветка**: `main`

### 2. Зависимости
В поле "Зависимости" укажите:
```
requirements_timeweb.txt
```

### 3. Команда запуска
В поле "Команда запуска" укажите:
```
python app.py
```

### 4. Переменные окружения
Добавьте следующие переменные:
```
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-super-secret-key-change-this-in-production-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
DEBUG=False
```

## Генерация SECRET_KEY

Выполните команду:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## После успешного деплоя

1. **Инициализируйте базу данных**:
   ```bash
   python init_timeweb.py
   ```

2. **Данные для входа**:
   - Логин: `admin`
   - Пароль: `admin123`

## Устранение проблем

### Если возникает "Deploy error":
1. Убедитесь, что используете `requirements_timeweb.txt`
2. Проверьте команду запуска: `python app.py`
3. Проверьте переменные окружения

### Если приложение не запускается:
1. Проверьте runtime логи
2. Убедитесь, что все переменные окружения заданы
3. Попробуйте команду: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Альтернативные команды запуска

Если `python app.py` не работает, попробуйте:

1. **uvicorn напрямую**:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **gunicorn**:
   ```
   gunicorn app.main:app --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker
   ```

## Готово! 🎉

После настройки приложение будет доступно по адресу:
`https://your-app-name.timeweb.cloud` 