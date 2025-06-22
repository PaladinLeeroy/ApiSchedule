#!/usr/bin/env python3
"""
Специальный файл запуска для Timeweb Cloud Apps
"""
import os
import sys
import uvicorn
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем приложение
from app.main import app

if __name__ == "__main__":
    # Получаем порт из переменной окружения или используем 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Запуск приложения на {host}:{port}")
    
    # Запускаем приложение
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    ) 