#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных и создания первого пользователя
"""
import sys
import os
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.database import init_db, SessionLocal
from app.api.models import User
from app.api.auth import get_password_hash
from config import settings

def init_database():
    """Инициализация базы данных"""
    print("Инициализация базы данных...")
    init_db()
    print("База данных инициализирована!")

def create_admin_user():
    """Создание администратора по умолчанию"""
    db = SessionLocal()
    try:
        # Проверяем, существует ли уже администратор
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Администратор уже существует!")
            return
        
        # Создаем администратора
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Администратор создан!")
        print("Логин: admin")
        print("Пароль: admin123")
        print("ВАЖНО: Измените пароль после первого входа!")
        
    except Exception as e:
        print(f"Ошибка при создании администратора: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Основная функция"""
    print("=== Инициализация системы управления расписанием ===")
    
    # Инициализируем базу данных
    init_database()
    
    # Создаем администратора
    create_admin_user()
    
    print("\n=== Инициализация завершена ===")
    print("Теперь вы можете запустить приложение:")
    print("python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 