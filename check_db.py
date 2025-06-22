import sqlite3
import os

def check_database(db_path):
    if not os.path.exists(db_path):
        print(f"База данных {db_path} не найдена!")
        return
    
    print(f"\n{'='*50}")
    print(f"Проверка базы данных: {db_path}")
    print(f"{'='*50}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Таблицы в базе данных: {tables}")
    
    # Проверяем содержимое каждой таблицы
    for table in tables:
        table_name = table[0]
        print(f"\n=== Таблица: {table_name} ===")
        
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Количество записей: {count}")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                print("Первые 5 записей:")
                for row in rows:
                    print(f"  {row}")
        except Exception as e:
            print(f"Ошибка при чтении таблицы {table_name}: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_database('app.db')
    check_database('test.db') 