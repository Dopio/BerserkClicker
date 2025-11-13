import os
import sqlite3


def reset_database():
    """Сбрасывает базу данных"""
    db_path = 'berserk_game.db'

    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Old database deleted!")

    # Создаем новую базу
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Таблица игроков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            blood INTEGER DEFAULT 0,
            kills INTEGER DEFAULT 0,
            damage INTEGER DEFAULT 1,
            health INTEGER DEFAULT 10,
            is_alive BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Таблица состояния игры
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            current_wave INTEGER DEFAULT 0,
            total_kills INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ New database created!")
    print("🎮 Restart Flask server to apply changes!")


if __name__ == "__main__":
    reset_database()