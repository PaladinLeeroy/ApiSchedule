#!/usr/bin/env python3
"""
Скрипт для проверки готовности проекта к развертыванию
"""
import os
import sys
import importlib
from pathlib import Path

def check_file_exists(file_path, description):
    """Проверка существования файла"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - НЕ НАЙДЕН")
        return False

def check_import(module_name, description):
    """Проверка возможности импорта модуля"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError:
        print(f"❌ {description}: {module_name} - НЕ УСТАНОВЛЕН")
        return False

def check_environment_variables():
    """Проверка переменных окружения"""
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'ALGORITHM',
        'ACCESS_TOKEN_EXPIRE_MINUTES'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Переменные окружения не настроены: {', '.join(missing_vars)}")
        print("   Создайте файл .env с необходимыми переменными")
        return False
    else:
        print("✅ Переменные окружения настроены")
        return True

def main():
    """Основная функция проверки"""
    print("=== Проверка готовности к развертыванию ===\n")
    
    # Проверка файлов
    files_to_check = [
        ("requirements.txt", "Файл зависимостей"),
        ("config.py", "Файл конфигурации"),
        ("app/main.py", "Главный файл приложения"),
        ("app/api/database.py", "Настройки базы данных"),
        ("app/api/auth.py", "Аутентификация"),
        ("gunicorn.conf.py", "Конфигурация Gunicorn"),
        ("Dockerfile", "Docker конфигурация"),
        ("docker-compose.yml", "Docker Compose"),
        ("Procfile", "Heroku конфигурация"),
        ("README.md", "Документация"),
        (".gitignore", "Git ignore"),
    ]
    
    file_checks = []
    for file_path, description in files_to_check:
        file_checks.append(check_file_exists(file_path, description))
    
    print()
    
    # Проверка зависимостей
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("alembic", "Alembic"),
        ("gunicorn", "Gunicorn"),
        ("python-dotenv", "Python-dotenv"),
        ("passlib", "Passlib"),
        ("jose", "PyJWT"),
        ("openpyxl", "OpenPyXL"),
        ("reportlab", "ReportLab"),
    ]
    
    dep_checks = []
    for module, description in dependencies:
        dep_checks.append(check_import(module, description))
    
    print()
    
    # Проверка переменных окружения
    env_check = check_environment_variables()
    
    print()
    print("=== Результаты проверки ===")
    
    all_files_ok = all(file_checks)
    all_deps_ok = all(dep_checks)
    
    if all_files_ok and all_deps_ok and env_check:
        print("🎉 Проект готов к развертыванию!")
        print("\nСледующие шаги:")
        print("1. Настройте переменные окружения в .env файле")
        print("2. Запустите: python init_database.py")
        print("3. Запустите: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
    else:
        print("⚠️  Проект требует доработки перед развертыванием")
        
        if not all_files_ok:
            print("- Проверьте наличие всех необходимых файлов")
        if not all_deps_ok:
            print("- Установите недостающие зависимости: pip install -r requirements.txt")
        if not env_check:
            print("- Настройте переменные окружения")

if __name__ == "__main__":
    main() 