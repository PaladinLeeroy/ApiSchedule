#!/usr/bin/env python3
"""
Скрипт для запуска миграций базы данных
"""
import os
import sys
import subprocess
from pathlib import Path

def run_migrations():
    """Запуск миграций Alembic"""
    try:
        # Проверяем, что мы в корневой директории проекта
        if not Path("alembic.ini").exists():
            print("Ошибка: alembic.ini не найден. Убедитесь, что вы находитесь в корневой директории проекта.")
            sys.exit(1)
        
        print("Запуск миграций Alembic...")
        
        # Запускаем миграции
        result = subprocess.run(["alembic", "upgrade", "head"], 
                              capture_output=True, text=True, check=True)
        
        print("Миграции успешно выполнены!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении миграций: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Ошибка: alembic не найден. Установите его: pip install alembic")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations() 