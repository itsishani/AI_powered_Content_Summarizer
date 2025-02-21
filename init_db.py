import sqlite3

def init_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publication_date TEXT,
            link TEXT NOT NULL UNIQUE,
            content TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
