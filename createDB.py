import sqlite3

class Database:
    def __init__(self):
        # Инициализация подключения к базе данных
        self.conn = sqlite3.connect('./testMBTI.db', isolation_level=None)
        self.cursor = self.conn.cursor()   

    def create_table_user_and_results(self):
        # Создание таблицы 'results' в базе данных, если она не существует
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS results (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                personality_type TEXT,
                                personality_value INTEGER,
                                ei INTEGER,
                                sn INTEGER,
                                tf INTEGER,
                                jp INTEGER)
                        ''')
    def insert_info(self, name, personality_type, personality_value, ei, sn, tf, jp):
        # Вставка информации в таблицу 'results'
        self.cursor.execute('''
                            INSERT INTO results (
                                name, 
                                personality_type, 
                                personality_value, 
                                ei, 
                                sn, 
                                tf, 
                                jp) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (name, personality_type, personality_value, ei, sn, tf, jp))
