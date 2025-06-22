#!/usr/bin/env python3
"""
Скрипт для генерации безопасного SECRET_KEY
"""
import secrets
import string
import base64
import os

def generate_secret_key(method="urlsafe", length=32):
    """
    Генерирует безопасный SECRET_KEY
    
    Args:
        method (str): Метод генерации ('urlsafe', 'hex', 'base64', 'alphanumeric')
        length (int): Длина ключа
    
    Returns:
        str: Сгенерированный SECRET_KEY
    """
    
    if method == "urlsafe":
        # URL-безопасная строка (рекомендуется для веб-приложений)
        return secrets.token_urlsafe(length)
    
    elif method == "hex":
        # Шестнадцатеричная строка
        return secrets.token_hex(length)
    
    elif method == "base64":
        # Base64 строка
        return base64.b64encode(secrets.token_bytes(length)).decode('utf-8')
    
    elif method == "alphanumeric":
        # Буквенно-цифровая строка
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    else:
        raise ValueError(f"Неизвестный метод: {method}")

def main():
    """Основная функция"""
    print("🔐 Генератор SECRET_KEY")
    print("=" * 50)
    
    # Генерируем разные варианты
    methods = {
        "urlsafe": "URL-безопасная строка (рекомендуется)",
        "hex": "Шестнадцатеричная строка",
        "base64": "Base64 строка",
        "alphanumeric": "Буквенно-цифровая строка"
    }
    
    for method, description in methods.items():
        key = generate_secret_key(method)
        print(f"\n📋 {description}:")
        print(f"SECRET_KEY={key}")
        print(f"Длина: {len(key)} символов")
    
    # Рекомендуемый вариант
    print("\n" + "=" * 50)
    print("🎯 РЕКОМЕНДУЕМЫЙ ВАРИАНТ для Timeweb:")
    recommended_key = generate_secret_key("urlsafe", 32)
    print(f"SECRET_KEY={recommended_key}")
    
    # Создаем файл .env с примером
    print("\n" + "=" * 50)
    print("📝 Создаю файл .env.example с примером:")
    
    env_content = f"""# Database Configuration
DATABASE_URL=sqlite:///./app.db

# Security (ОБЯЗАТЕЛЬНО ИЗМЕНИТЕ В ПРОДАКШЕНЕ!)
SECRET_KEY={recommended_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Environment
ENVIRONMENT=production
"""
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Файл .env.example создан!")
    print("\n💡 Используйте этот SECRET_KEY в настройках Timeweb Cloud Apps")

if __name__ == "__main__":
    main() 