import multiprocessing
import sys
import os

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

# Количество воркеров
workers = multiprocessing.cpu_count() * 2 + 1

# Тип воркера
worker_class = "uvicorn.workers.UvicornWorker"

# Биндинг
bind = f"{settings.HOST}:{settings.PORT}"

# Таймауты
timeout = 120
keepalive = 2

# Логирование
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Перезагрузка при изменении файлов (только для разработки)
reload = settings.DEBUG

# Максимальное количество запросов на воркера
max_requests = 1000
max_requests_jitter = 50

# Предзагрузка приложения
preload_app = True

# Пользователь и группа (для Linux)
# user = "www-data"
# group = "www-data" 