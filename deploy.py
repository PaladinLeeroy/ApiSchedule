#!/usr/bin/env python3
"""
Скрипт для автоматического развертывания проекта
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Выполнение команды с выводом"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} завершено успешно")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description}: {e}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def create_env_file():
    """Создание файла .env из примера"""
    if not Path(".env").exists():
        if Path("env.example").exists():
            shutil.copy("env.example", ".env")
            print("✅ Файл .env создан из env.example")
            print("⚠️  ВАЖНО: Измените SECRET_KEY в файле .env перед продакшеном!")
        else:
            print("❌ Файл env.example не найден")
            return False
    else:
        print("✅ Файл .env уже существует")
    return True

def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Требуется Python 3.8+, текущая версия: {version.major}.{version.minor}")
        return False
    print(f"✅ Версия Python: {version.major}.{version.minor}.{version.micro}")
    return True

def main():
    """Основная функция развертывания"""
    print("=== Автоматическое развертывание системы управления расписанием ===\n")
    
    # Проверка версии Python
    if not check_python_version():
        sys.exit(1)
    
    # Создание файла .env
    if not create_env_file():
        sys.exit(1)
    
    print("\n=== Установка зависимостей ===")
    
    # Обновление pip
    run_command("python -m pip install --upgrade pip", "Обновление pip")
    
    # Установка зависимостей
    if not run_command("pip install -r requirements.txt", "Установка зависимостей"):
        print("❌ Ошибка при установке зависимостей")
        sys.exit(1)
    
    print("\n=== Инициализация базы данных ===")
    
    # Инициализация базы данных
    if not run_command("python init_database.py", "Инициализация базы данных"):
        print("❌ Ошибка при инициализации базы данных")
        sys.exit(1)
    
    print("\n=== Проверка готовности ===")
    
    # Проверка готовности
    if not run_command("python check_deployment.py", "Проверка готовности"):
        print("❌ Проект не готов к развертыванию")
        sys.exit(1)
    
    print("\n=== Развертывание завершено успешно! ===")
    print("\n🎉 Проект готов к запуску!")
    print("\nКоманды для запуска:")
    print("📝 Для разработки:")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n🚀 Для продакшена:")
    print("   gunicorn -c gunicorn.conf.py app.main:app")
    print("\n🐳 Для Docker:")
    print("   docker-compose up -d")
    print("\n📱 Доступ к приложению: http://localhost:8000")
    print("👤 Логин администратора: admin")
    print("🔑 Пароль администратора: admin123")
    print("\n⚠️  ВАЖНО: Измените пароль администратора после первого входа!")

if __name__ == "__main__":
    main() 