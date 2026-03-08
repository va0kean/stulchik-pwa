import os
import sqlite3

SOURCE_DIR = r'C:\Android\stulchik\app\src\main\assets\articles'
DB_PATH = r'C:\Project\stulchik-pwa\archive.db'


def process_files():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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

    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.txt')]
    print(f"Обработка {len(files)} файлов...")

    for filename in files:
        path = os.path.join(SOURCE_DIR, filename)
        try:
            with open(path, 'r', encoding='cp1251', errors='replace') as f:
                lines = f.readlines()
                if len(lines) < 3:
                    continue

                category_line = lines[0].split(':', 1)[1].strip() if ':' in lines[0] else lines[0].strip()
                author = lines[1].split(':', 1)[1].strip() if ':' in lines[1] else lines[1].strip()
                title = lines[2].split(':', 1)[1].strip() if ':' in lines[2] else lines[2].strip()
                text = "".join(lines[3:]).strip()

                categories = [c.strip() for c in category_line.split(',')]
                for cat in categories:
                    cursor.execute('''
                        INSERT INTO articles (file_name, category, author, title, content)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (filename, cat, author, title, text))
        except Exception as e:
            print(f"Ошибка {filename}: {e}")

    conn.commit()
    cursor.execute("VACUUM")
    conn.close()

    new_size = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"Готово! Новый размер базы: {new_size:.2f} MB")


if __name__ == "__main__":
    process_files()