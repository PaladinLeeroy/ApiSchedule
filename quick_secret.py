#!/usr/bin/env python3
"""
Быстрая генерация SECRET_KEY для Timeweb Cloud Apps
"""
import secrets

# Генерируем безопасный SECRET_KEY
secret_key = secrets.token_urlsafe(32)

print("🔐 Быстрая генерация SECRET_KEY")
print("=" * 40)
print(f"SECRET_KEY={secret_key}")
print("=" * 40)
print("💡 Скопируйте этот ключ в настройки Timeweb Cloud Apps")
print("⚠️  НЕ ДЕЛИТЕСЬ этим ключом с другими!") 