import os
import sqlite3

# Пути (проверьте правильность перед запуском)
SOURCE_DIR = r'C:\Android\stulchik\app\src\main\assets\articles'
DB_PATH = r'C:\Project\stulchik-pwa\archive.db'

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH) # Пересоздаем базу с нуля
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Таблица со всеми данными
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            category TEXT,
            author TEXT,
            title TEXT,
            content TEXT,
            status INTEGER DEFAULT 0
        )
    ''')
    return conn, cursor

def process_files():
    conn, cursor = create_db()
    # Фильтруем файлы по расширению .txt
    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.txt')]
    
    print(f"Найдено файлов: {len(files)}. Начинаю конвертацию...")

    for filename in files:
        path = os.path.join(SOURCE_DIR, filename)
        try:
            # Читаем в ANSI (cp1251), как вы указали
            with open(path, 'r', encoding='cp1251', errors='replace') as f:
                lines = f.readlines()
                
                if len(lines) < 3: continue # Пропуск пустых файлов

                # Извлекаем метаданные (удаляем префиксы "Категория:", "Автор:", "Название:")
                category_line = lines[0].split(':', 1)[1].strip() if ':' in lines[0] else lines[0].strip()
                author = lines[1].split(':', 1)[1].strip() if ':' in lines[1] else lines[1].strip()
                title = lines[2].split(':', 1)[1].strip() if ':' in lines[2] else lines[2].strip()
                
                # Текст статьи начинается с 4-й строки
                content = "".join(lines[3:]).strip()

                # Задача 2: Разделяем категории по запятой
                categories = [c.strip() for c in category_line.split(',')]
                
                for cat in categories:
                    cursor.execute('''
                        INSERT INTO articles (file_name, category, author, title, content)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (filename, cat, author, title, content))
        except Exception as e:
            print(f"Ошибка в файле {filename}: {e}")

    conn.commit()
    conn.close()
    print(f"Успех! База создана: {DB_PATH}")

if __name__ == "__main__":
    process_files()