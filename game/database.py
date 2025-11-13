import psycopg2


class PostgresDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
        self.init_database()

    @staticmethod
    def get_connection_params():
        return {
            "host": "localhost",
            "database": "berserk_game",
            "user": "postgres",  # ← ЭТОГО НЕ ХВАТАЛО!
            "password": "adrenalin9543",
            "port": "5432"
        }

    def connect(self):
        try:
            params = self.get_connection_params()
            self.connection = psycopg2.connect(**params)
            print('Connected to PostgresSQL!')
        except Exception as e:
            print(f'Connection error: {e}')
            print("Проверь:")
            print("  - Запущен ли PostgresSQL?")
            print("  - Правильный ли пароль?")
            print("  - Существует ли база 'berserk_game'?")

    def get_connection(self):
        try:
            if self.connection and self.connection.closed == 0:
                return self.connection
            else:
                self.connect()
                return self.connection
        except Exception as e:  # ← добавил Exception as e
            print(f"❌ Connection error in get_connection: {e}")
            self.connect()
            return self.connection

    def init_database(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    blood INTEGER DEFAULT 0,
                    kills INTEGER DEFAULT 0,
                    damage INTEGER DEFAULT 1,
                    health INTEGER DEFAULT 10,
                    is_alive BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS game_state (
                            id SERIAL PRIMARY KEY,
                            player_name VARCHAR(100) REFERENCES players(name),
                            current_wave INTEGER DEFAULT 0,
                            total_kills INTEGER DEFAULT 0,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')
            conn.commit()
            cursor.close()
            print('PostgresSQL tables created!')

        except Exception as e:
            print(f'Error creating tables: {e}')

    def save_player(self, player_data):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO players (name, blood, kills, damage, health, is_alive)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (name) 
                DO UPDATE SET 
                    blood = EXCLUDED.blood,
                    kills = EXCLUDED.kills, 
                    damage = EXCLUDED.damage,
                    health = EXCLUDED.health,
                    is_alive = EXCLUDED.is_alive
                ''', (
                player_data['name'], player_data['blood'],
                player_data['kills'], player_data['damage'],
                player_data['health'], player_data['is_alive']
            ))

            conn.commit()
            cursor.close()
            print('Player saved to PostgresSQL')
            return True

        except Exception as e:
            print(f'Error saving player: {e}')
            return False

    def load_player(self, player_name="Guts"):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT name, blood, kills, damage, health, is_alive 
                FROM players WHERE name = %s
            ''', (player_name,))

            player_data = cursor.fetchone()
            cursor.close()

            if player_data:
                return {
                    'name': player_data[0],
                    'blood': player_data[1],
                    'kills': player_data[2],
                    'damage': player_data[3],
                    'health': player_data[4],
                    'max_health': player_data[4],
                    'is_alive': player_data[5]
                }
            return None

        except Exception as e:
            print(f"Error loading player: {e}")
            return None

    def save_game_state(self, player_name, current_wave, total_kills):
        """Сохраняет состояние игры"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Удаляем старую запись и вставляем новую
            cursor.execute('DELETE FROM game_state WHERE player_name = %s', (player_name,))
            cursor.execute('''
                INSERT INTO game_state (player_name, current_wave, total_kills)
                VALUES (%s, %s, %s)
            ''', (player_name, current_wave, total_kills))

            conn.commit()
            cursor.close()
            print("💾 Game state saved to PostgreSQL!")
            return True

        except Exception as e:
            print(f"❌ Error saving game state: {e}")
            return False

    def load_game_state(self, player_name='Guts'):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT current_wave, total_kills 
                FROM game_state WHERE player_name = %s
            ''', (player_name,))
            state_data = cursor.fetchhone()
            cursor.close()

            if state_data:
                return {
                    'current_wave': state_data[0],
                    'total_kills': state_data[1]
                }
            return None

        except Exception as e:
            print(f'Error loading game state: {e}')
            return None
