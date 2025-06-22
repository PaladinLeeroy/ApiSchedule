import requests
import sys

def create_user(username, password, role):
    url = "http://127.0.0.1:8000/register"
    data = {
        "username": username,
        "password": password,
        "role": role
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        print(f"Пользователь {username} успешно создан!")
        print(f"Роль: {role}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при создании пользователя: {e}")
        if hasattr(e.response, 'json'):
            print(f"Детали ошибки: {e.response.json()}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python create_user.py <username> <password> <role>")
        print("Пример: python create_user.py admin password123 admin")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    role = sys.argv[3]
    
    # Проверяем, что роль одна из допустимых
    valid_roles = ["admin", "teacher", "student"]
    if role not in valid_roles:
        print(f"Ошибка: роль должна быть одной из {valid_roles}")
        sys.exit(1)
    
    create_user(username, password, role) 