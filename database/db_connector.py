"""
# DineMate Database Connector 🗄️

This module provides a utility to test database connectivity and verify data.

Dependencies:
- sqlite3: For database operations 🗄️.
- logger: For structured logging 📜.
- config: For database configuration ⚙️.
"""

import sqlite3
from scripts.logger import get_logger

logger = get_logger(__name__)

def test_database(db_path: str = "foodbot.db") -> None:
    """🗄️ Test database connectivity and print table contents.

    Args:
        db_path (str): Path to the SQLite database file.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            logger.info({"db_path": db_path, "message": "Connected to SQLite database for testing"})

            # Test menu table
            # cursor.execute("SELECT * FROM menu")
            # menu_rows = cursor.fetchall()
            # logger.info({"table": "menu", "rows": len(menu_rows), "message": "Fetched menu data"})
            # print("✅ Menu Items:")
            # for row in menu_rows:
            #     print(row)

            # Test orders table
            cursor.execute("SELECT * FROM orders")
            order_rows = cursor.fetchall()
            logger.info({"table": "orders", "rows": len(order_rows), "message": "Fetched orders data"})
            print("\n✅ Orders:")
            for row in order_rows:
                print(row)

            # Test staff table
            # cursor.execute("SELECT * FROM staff")
            # staff_rows = cursor.fetchall()
            # logger.info({"table": "staff", "rows": len(staff_rows), "message": "Fetched staff data"})
            # print("\n✅ Staff:")
            # for row in staff_rows:
            #     print(row)

            # Test customers table
            # cursor.execute("SELECT * FROM customers")
            # customer_rows = cursor.fetchall()
            # logger.info({"table": "customers", "rows": len(customer_rows), "message": "Fetched customers data"})
            # print("\n✅ Customers:")
            # for row in customer_rows:
            #     print(row)

    except sqlite3.Error as e:
        logger.error({"error": str(e), "message": "Failed to connect or fetch data"})
        raise
    except Exception as e:
        logger.error({"error": str(e), "message": "Unexpected error in database testing"})
        raise

if __name__ == "__main__":
    test_database()