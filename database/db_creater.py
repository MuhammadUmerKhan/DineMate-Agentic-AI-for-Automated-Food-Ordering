import sqlite3
# from config import *

conn = sqlite3.connect("./foodbot.db")  # ✅ Create SQLite DB
cursor = conn.cursor()

with open("./foodbot_schemalite.sql", "r") as f:
    cursor.executescript(f.read())  # ✅ Run SQL file

conn.commit()
conn.close()

print("✅ Database and tables created successfully!")