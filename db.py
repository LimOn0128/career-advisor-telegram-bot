import sqlite3
import os

DB_NAME = 'career.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        skills TEXT,
        education TEXT,
        salary_range TEXT,
        category TEXT,
        interests TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        age_group TEXT,
        interests TEXT,
        current_job TEXT,
        recommendations TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        profession_ids TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def load_initial_data(sql_file='data/professions.sql'):
    # Получаем директорию, в которой лежит db.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, sql_file)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with open(full_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

def get_professions_by_category(category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM professions WHERE category = ?', (category,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_professions_by_interests(interests):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    like_clause = ' OR '.join([f'interests LIKE "%{interest}%"' for interest in interests.split(',')])
    cursor.execute(f'SELECT * FROM professions WHERE {like_clause}')
    results = cursor.fetchall()
    conn.close()
    return results

def save_user_data(user_id, age_group, interests, current_job):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, age_group, interests, current_job)
    VALUES (?, ?, ?, ?)
    ''', (user_id, age_group, interests, current_job))
    conn.commit()
    conn.close()

def get_user_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result


if __name__ == '__main__':
    init_db()
    # Загружаем начальные данные ТОЛЬКО если таблица пустая
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM professions")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        try:
            load_initial_data('data/professions.sql')
            print("Начальные профессии успешно загружены")
        except Exception as e:
            print("Ошибка при загрузке начальных данных:", e)


if __name__ == '__main__':
    init_db()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM professions")
    count = cursor.fetchone()[0]
    print(f"Профессий в базе после запуска: {count}")
    
    if count > 0:
        cursor.execute("SELECT name, category FROM professions LIMIT 3")
        print("Примеры профессий:", cursor.fetchall())
        
        # Инициализируем БД при запуске
init_db()
# Если нужно, загрузите начальные данные: load_initial_data()

