"""
# DineMate Database Creator 🗄️

This module creates and populates the DineMate SQLite database with optimized schema and rich data.

Dependencies:
- sqlite3: For database operations 🗄️.
- json: For JSON serialization 🗃️.
- bcrypt: For password hashing 🔒.
- datetime: For timestamp generation 🕒.
- random: For generating varied data 🎲.
- logger: For structured logging 📜.
- config: For database configuration ⚙️.
- os: For file path validation 🗂️.
- faker: For realistic data generation 🌟.
"""

import sqlite3
import json
import bcrypt
import datetime
import random
import os
from typing import List, Dict
from scripts.logger import get_logger
# from config import DB_PATH
from faker import Faker

# Initialize logger and Faker
logger = get_logger(__name__)
fake = Faker()

def create_database(db_path: str = "foodbot.db") -> None:
    """🗄️ Create and populate the SQLite database.

    Args:
        db_path (str): Path to the SQLite database file.
        schema_path (str): Path to the SQL schema file.
    """
    try:
        # Validate schema file
        # if not os.path.exists(schema_path):
        #     logger.error({"schema_path": schema_path, "message": "Schema file not found"})
        #     raise FileNotFoundError(f"Schema file {schema_path} not found")

        # Connect to database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            logger.info({"db_path": db_path, "message": "Connected to SQLite database"})

            # Execute schema
            # with open(schema_path, "r") as f:
            #         cursor.executescript(f.read())  # ✅ Run SQL file
            # logger.info({"schema_path": schema_path, "message": "Schema executed successfully"})

            # Populate tables
            # populate_menu(cursor)
            populate_orders(cursor, use_defaults=False)  # Use varied timestamps for rich analysis
            # populate_users(cursor)
            conn.commit()
            logger.info({"message": "Database populated successfully"})

        print("✅ Database and tables created successfully!")

    except sqlite3.Error as e:
        logger.error({"error": str(e), "message": "Failed to create/populate database"})
        raise
    except Exception as e:
        logger.error({"error": str(e), "message": "Unexpected error in database creation"})
        raise

def populate_menu(cursor: sqlite3.Cursor) -> None:
    """🍽️ Populate the menu table with items and prices."""
    menu_items = [
        ("cheese burger", 5.99), ("chicken burger", 6.99), ("veggie burger", 5.49),
        ("pepperoni pizza", 12.99), ("margherita pizza", 11.49), ("bbq chicken pizza", 13.99),
        ("grilled chicken sandwich", 7.99), ("club sandwich", 6.99), ("spaghetti carbonara", 9.99),
        ("fettuccine alfredo", 10.49), ("tandoori chicken", 11.99), ("butter chicken", 12.49),
        ("beef steak", 15.99), ("chicken biryani", 8.99), ("mutton biryani", 10.99),
        ("prawn curry", 13.49), ("fish and chips", 9.49), ("french fries", 3.99),
        ("garlic bread", 4.49), ("chocolate brownie", 5.49), ("vanilla ice cream", 3.99),
        ("strawberry shake", 4.99), ("mango smoothie", 5.49), ("coca-cola", 2.49),
        ("pepsi", 2.49), ("fresh orange juice", 4.99)
    ]
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO menu (name, price) VALUES (?, ?)",
            menu_items
        )
        logger.info({"count": len(menu_items), "message": "Menu items inserted"})
    except sqlite3.Error as e:
        logger.error({"error": str(e), "message": "Failed to populate menu"})
        raise

def populate_orders(cursor: sqlite3.Cursor, use_defaults: bool = False) -> None:
    """📦 Populate the orders table with diverse data.

    Args:
        cursor (sqlite3.Cursor): Database cursor.
        use_defaults (bool): If True, use schema defaults for date and time; else, generate varied timestamps.
    """
    # Fetch menu for price calculations
    cursor.execute("SELECT name, price FROM menu")
    menu_dict = {row[0]: row[1] for row in cursor.fetchall()}
    
    statuses = ["Pending", "Preparing", "In Process", "Ready", "Completed", "Delivered", "Canceled"]
    status_weights = [0.1, 0.1, 0.1, 0.1, 0.2, 0.4, 0.1]  # Realistic distribution
    
    orders = []
    for _ in range(150):  # Generate 150 orders
        # Generate items and total price
        num_items = random.randint(1, 5)
        order_items = random.sample(list(menu_dict.keys()), num_items)
        order_dict = {item: random.randint(1, 3) for item in order_items}
        total_price = sum(menu_dict[item] * qty for item, qty in order_dict.items())
        status = random.choices(statuses, weights=status_weights, k=1)[0]
        
        if use_defaults:
            # Use schema defaults for date and time
            orders.append((json.dumps(order_dict), total_price, status))
        else:
            # Generate varied date (2023–2025) and time (8 AM–11 PM)
            order_date = fake.date_between(start_date=datetime.date(2023, 1, 1), end_date=datetime.date(2025, 7, 7))
            order_time = fake.time_object().replace(hour=random.randint(8, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
            order_time_str = order_time.strftime("%I:%M:%S %p")
            orders.append((
                json.dumps(order_dict),
                total_price,
                status,
                order_date.strftime("%Y-%m-%d"),
                order_time_str
            ))
    
    try:
        if use_defaults:
            cursor.executemany(
                "INSERT INTO orders (items, total_price, status) VALUES (?, ?, ?)",
                orders
            )
        else:
            cursor.executemany(
                "INSERT INTO orders (items, total_price, status, date, time) VALUES (?, ?, ?, ?, ?)",
                orders
            )
        logger.info({"count": len(orders), "use_defaults": use_defaults, "message": "Orders inserted"})
    except sqlite3.Error as e:
        logger.error({"error": str(e), "message": "Failed to populate orders"})
        raise

def populate_users(cursor: sqlite3.Cursor) -> None:
    """👤 Populate staff and customers tables with sample users."""
    # Staff
    staff = [
        ("admin", bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "admin"),
        ("chef", bcrypt.hashpw("chef123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "kitchen_staff"),
        ("support", bcrypt.hashpw("support123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "customer_support"),
    ]
    
    # Customers
    customers = [
        (f"user{i}", bcrypt.hashpw(f"pass{i}".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), f"user{i}@example.com")
        for i in range(1, 11)
    ]
    
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO staff (username, password_hash, role) VALUES (?, ?, ?)",
            staff
        )
        cursor.executemany(
            "INSERT OR IGNORE INTO customers (username, password_hash, email) VALUES (?, ?, ?)",
            customers
        )
        logger.info({"staff_count": len(staff), "customer_count": len(customers), "message": "Users inserted"})
    except sqlite3.Error as e:
        logger.error({"error": str(e), "message": "Failed to populate users"})
        raise

if __name__ == "__main__":
    create_database()