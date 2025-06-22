import multiprocessing
import sys
import os

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

# Количество воркеров (адаптировано для Timeweb)
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # Максимум 4 воркера

# Тип воркера
worker_class = "uvicorn.workers.UvicornWorker"

# Биндинг
bind = f"{settings.HOST}:{settings.PORT}"

# Таймауты (увеличены для Timeweb)
timeout = 300
keepalive = 5

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

# Настройки для Timeweb Cloud Apps
worker_connections = 1000
backlog = 2048

# Graceful timeout для корректного завершения
graceful_timeout = 30

# Пользователь и группа (для Linux)
# user = "www-data"
# group = "www-data" 