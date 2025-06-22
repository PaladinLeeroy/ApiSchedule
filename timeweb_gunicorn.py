#!/usr/bin/env python3
"""
Альтернативный файл запуска с gunicorn для Timeweb Cloud Apps
"""
import os
import sys
import multiprocessing
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем приложение
from app.main import app

# Настройки для Timeweb
bind = f"0.0.0.0:{os.getenv('PORT', 8000)}"
workers = min(multiprocessing.cpu_count() * 2 + 1, 2)  # Максимум 2 воркера для Timeweb
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Логирование
accesslog = "-"
errorlog = "-"
loglevel = "info"

if __name__ == "__main__":
    from gunicorn.app.wsgiapp import WSGIApplication
    
    # Создаем WSGI приложение
    class StandaloneApplication(WSGIApplication):
        def __init__(self, app_uri, options=None):
            self.options = options or {}
            self.app_uri = app_uri
            super().__init__()
        
        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key, value)
    
    # Запускаем gunicorn
    StandaloneApplication(
        "timeweb_gunicorn:app",
        {
            "bind": bind,
            "workers": workers,
            "worker_class": worker_class,
            "timeout": timeout,
            "keepalive": keepalive,
            "max_requests": max_requests,
            "max_requests_jitter": max_requests_jitter,
            "preload_app": preload_app,
            "accesslog": accesslog,
            "errorlog": errorlog,
            "loglevel": loglevel,
        }
    ).run() 