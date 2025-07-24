import sqlite3

DB_NAME = 'agelink.db'

with sqlite3.connect(DB_NAME) as conn: 
    c = conn.cursor()
    c.execute("ALTER TABLE users ADD COLUMN age INTEGER")
    c.execute("ALTER TABLE users ADD COLUMN bio TEXT")
    c.execute("ALTER TABLE users ADD COLUMN interests TEXT")
    conn.commit()
