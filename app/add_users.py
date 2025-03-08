from database.MySQL_db import Database

db = Database()

# ✅ Add admin, kitchen staff, and customer support users
print(db.add_user("admin", "admin123", "admin"))
print(db.add_user("chef", "chef123", "kitchen_staff"))
print(db.add_user("support", "support123", "customer_support"))