from flask_login import UserMixin
import sqlite3

DB_NAME = 'agelink.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS connections (
                user_id INTEGER,
                friend_id INTEGER,
                UNIQUE(user_id, friend_id)
            )
        ''')
        conn.commit()

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get_by_username(username):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            if row:
                return User(*row)
        return None

    @staticmethod
    def get_by_id(user_id):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
            row = c.fetchone()
            if row:
                return User(*row)
        return None

    @staticmethod
    def create(username, password):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

    @staticmethod 
    def get_all_except(user_id):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users WHERE id != ?", (user_id,))
            rows = c.fetchall()
            return [User(*row) for row in rows]

    @staticmethod
    def add_connection(user_id, friend_id):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO connections (user_id, friend_id) VALUES (?, ?)", (user_id, friend_id))
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # Already connected, ignore

    @staticmethod
    def is_connected(user_id, friend_id):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM connections WHERE user_id = ? AND friend_id = ?", (user_id, friend_id))
            return c.fetchone() is not None

    @staticmethod
    def get_connections(user_id):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''
                SELECT u.id, u.username, u.password
                FROM users u
                JOIN connections c ON c.friend_id = u.id
                WHERE c.user_id = ?
            ''', (user_id,))
            rows = c.fetchall()
            return [User(*row) for row in rows]
