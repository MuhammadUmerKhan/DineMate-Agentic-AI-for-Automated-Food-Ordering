import sqlite3
# from config import *

# ✅ Connect to SQLite database
conn = sqlite3.connect("./foodbot.db")
cursor = conn.cursor()

# ✅ Retrieve all menu items
cursor.execute("SELECT * FROM staff")
rows = cursor.fetchall()  # Fetch all results

# ✅ Print results
for row in rows:
    print(row)  # (id, name, price)

# ✅ Close connection
conn.close()