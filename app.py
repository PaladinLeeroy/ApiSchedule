#!/usr/bin/env python3
"""
Минимальный файл запуска для Timeweb Cloud Apps
"""
import os
import sys
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Импортируем приложение
    from app.main import app
    
    if __name__ == "__main__":
        import uvicorn
        
        # Получаем порт из переменной окружения или используем 8000
        port = int(os.getenv("PORT", 8000))
        host = os.getenv("HOST", "0.0.0.0")
        
        print(f"🚀 Запуск приложения на {host}:{port}")
        print(f"📁 Рабочая директория: {os.getcwd()}")
        print(f"🐍 Python версия: {sys.version}")
        
        # Запускаем приложение
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
        
except Exception as e:
    print(f"❌ Ошибка при запуске: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 