#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных на Timeweb Cloud Apps
"""
import os
import sys
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.database import init_db, get_db
from app.api.models import User
from app.api.auth import get_password_hash
from sqlalchemy.orm import Session

def init_timeweb_database():
    """Инициализация базы данных для Timeweb"""
    print("🚀 Инициализация базы данных для Timeweb Cloud Apps...")
    
    try:
        # Инициализируем базу данных
        init_db()
        print("✅ База данных инициализирована")
        
        # Создаем пользователя-администратора
        db = next(get_db())
        
        # Проверяем, существует ли уже админ
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Пользователь-администратор создан")
            print("   Логин: admin")
            print("   Пароль: admin123")
        else:
            print("ℹ️  Пользователь-администратор уже существует")
        
        db.close()
        print("🎉 Инициализация завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_timeweb_database() 