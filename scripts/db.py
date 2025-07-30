"""
DineMate Database Operations 🗄️

Handles all SQLite interactions for DineMate.

Dependencies:
- sqlite3
- datetime
- json
- bcrypt
- pandas
- logger (custom)
- config (DB_PATH)
"""

import sqlite3, datetime, json, bcrypt, pandas as pd
from typing import Dict, Optional
from scripts.logger import get_logger
from scripts.config import DB_PATH

logger = get_logger(__name__)

class Database:
    def __init__(self, db_path: str=DB_PATH):
        """🗄️ Initialize and connect to SQLite database."""
        try:
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.info("✅ Connected to SQLite database")
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Database connection failed"})
            raise

    def fetch_order_data(self, status: Optional[str] = "Delivered") -> pd.DataFrame:
        """📦 Fetch orders as DataFrame filtered by status.

        Args:
            status (Optional[str]): Order status or 'All'.

        Returns:
            pd.DataFrame: Resulting DataFrame or empty if error.
        """
        logger.info("📊 Fetching order data for analytics")
        query = "SELECT id, items, total_price, status, date, time FROM orders"
        try:
            if status and status != "All":
                query += " WHERE status = ?"
                return pd.read_sql_query(query, self.connection, params=(status,))
            return pd.read_sql_query(query, self.connection)
        except Exception as e:
            logger.error({"error": str(e), "message": "❌ Error fetching order data"})
            return pd.DataFrame()

    def load_menu(self) -> Optional[Dict[str, float]]:
        """🍽️ Load menu items as a compact dictionary.

        Returns:
            Optional[Dict[str, float]]: Dictionary of item names to prices or None if error.
        """
        try:
            self.cursor.execute("SELECT name, price FROM menu")
            menu = {row["name"]: float(row["price"]) for row in self.cursor.fetchall()}
            logger.info("🍔 Fetched menu items")
            return menu if menu else None
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Error fetching menu"})
            return None

    def get_max_id(self) -> int:
        """🔢 Get next available order ID.

        Returns:
            int: Next order ID.
        """
        try:
            self.cursor.execute("SELECT MAX(id) FROM orders")
            result = self.cursor.fetchone()
            return (result[0] or 0) + 1
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Error fetching max ID"})
            return 1

    def store_order_db(self, order_dict: Dict[str, int], price: float, status: str = "Pending") -> Optional[int]:
        """📝 Store a new order.

        Args:
            order_dict (Dict[str, int]): Items with quantities.
            price (float): Total order price.
            status (str): Order status.

        Returns:
            Optional[int]: New order ID or None on error.
        """
        try:
            now = datetime.datetime.now()
            order_id = self.get_max_id()
            self.cursor.execute(
                """
                INSERT INTO orders (id, items, total_price, status, date, time)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (order_id, json.dumps(order_dict), price, status, now.strftime("%Y-%m-%d"), now.strftime("%I:%M:%S %p"))
            )
            self.connection.commit()
            logger.info("✅ Order stored")
            return order_id
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Error storing order"})
            return None

    def check_order_status_db(self, order_id: int) -> str:
        """🔍 Check order status and delivery time.

        Args:
            order_id (int): Order ID.

        Returns:
            str: Status message.
        """
        logger.info("📦 Checking order status")
        try:
            self.cursor.execute("SELECT status, time, date FROM orders WHERE id = ?", (order_id,))
            row = self.cursor.fetchone()
            if not row:
                return f"No order found with ID {order_id}"

            status = row["status"]
            if status in {"Canceled", "Delivered"}:
                return f"Order {order_id} is {status.lower()}."

            order_time = datetime.datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %I:%M:%S %p")
            estimated_time = order_time + datetime.timedelta(minutes=40)
            now = datetime.datetime.now()

            if now > estimated_time:
                delay = int((now - estimated_time).total_seconds() / 60)
                return f"Status: {status}, Delivery: {estimated_time.strftime('%I:%M %p')} (delayed ~{delay} min)"
            return f"Status: {status}, Delivery: {estimated_time.strftime('%I:%M %p')}"
        except Exception as e:
            logger.error({"error": str(e), "message": "❌ Error fetching status"})
            return f"Error: {e}"

    def cancel_order_after_confirmation(self, order_id: int) -> str:
        """❌ Cancel an order if within 10 minutes.

        Args:
            order_id (int): Order ID.

        Returns:
            str: Result message.
        """
        logger.info("🚫 Checking cancellation")
        try:
            self.cursor.execute("SELECT status, date, time FROM orders WHERE id = ?", (order_id,))
            row = self.cursor.fetchone()
            if not row:
                return f"No order found with ID {order_id}"

            if row["status"] in {"Canceled", "Completed", "Delivered"}:
                return f"Order {order_id} is {row['status'].lower()}."

            order_time = datetime.datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %I:%M:%S %p")
            if (datetime.datetime.now() - order_time).total_seconds() > 600:
                return "Cannot cancel: past 10-min window."

            self.cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Canceled", order_id))
            self.connection.commit()
            return f"Order {order_id} canceled."
        except Exception as e:
            logger.error({"error": str(e), "message": "❌ Error canceling"})
            return f"Error: {e}"

    def modify_order_after_confirmation(self, order_id: int, updated_items: str, new_total_price: float) -> str:
        """✏️ Modify order if within 10 minutes.

        Args:
            order_id (int): Order ID.
            updated_items (str): JSON string of items and quantities.
            new_total_price (float): New price.

        Returns:
            str: Status message.
        """
        logger.info("✍️ Checking modification")
        try:
            items = json.loads(updated_items)
            if not items:
                return "⚠️ No items provided."

            menu = self.load_menu() or []
            valid_items = {item["name"].lower() for item in menu}
            for item in items:
                if item.lower() not in valid_items:
                    return f"⚠️ '{item}' not in menu."

            self.cursor.execute("SELECT status, date, time FROM orders WHERE id = ?", (order_id,))
            row = self.cursor.fetchone()
            if not row:
                return f"⚠️ No order found with ID {order_id}."

            if row["status"] not in {"Pending", "Preparing"}:
                return f"⚠️ Order {order_id} is {row['status'].lower()}."

            order_time = datetime.datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %I:%M:%S %p")
            if (datetime.datetime.now() - order_time).total_seconds() > 600:
                return "⚠️ Cannot modify: past 10-min window."

            self.cursor.execute(
                "UPDATE orders SET items = ?, total_price = ? WHERE id = ?",
                (json.dumps(items), new_total_price, order_id)
            )
            self.connection.commit()

            summary = ", ".join(f"{item}: {qty}" for item, qty in items.items())
            return f"✅ Order {order_id} updated. Items: {summary}, Total: ${new_total_price:.2f}"
        except (sqlite3.Error, ValueError, TypeError) as e:
            logger.error({"error": str(e), "message": "❌ Failed to update"})
            return f"⚠️ Error: {str(e)}"

    def get_order_by_id(self, order_id: int) -> Dict[str, any]:
        """🔍 Get full order details.

        Args:
            order_id (int): Order ID.

        Returns:
            Dict[str, any]: Order dict with message.
        """
        logger.info("🔎 Fetching order details")
        try:
            self.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = self.cursor.fetchone()
            if not row:
                return {"status": "error", "message": f"No order found with ID {order_id}"}

            order = dict(row)
            items = json.loads(order["items"])
            msg = f"Order {order_id}: {', '.join(f'{k}: {v}' for k,v in items.items())}, Total: ${order['total_price']:.2f}, Status: {order['status']}"

            if order["status"] == "Pending":
                placed = datetime.datetime.strptime(f"{order['date']} {order['time']}", "%Y-%m-%d %I:%M:%S %p")
                minutes = (datetime.datetime.now() - placed).total_seconds() / 60
                msg += f"\n{int(10 - minutes)} min to modify" if minutes <= 10 else "\nCannot modify: past 10-min window."
            else:
                msg += f"\nCannot modify: order is {order['status'].lower()}."

            order.update({"items": items, "message": msg})
            return order
        except Exception as e:
            logger.error({"error": str(e), "message": "❌ Error fetching order"})
            return {"status": "error", "message": f"Error: {e}"}

    def add_user(self, username: str, password: str, email: str, role: str = "customer") -> str:
        """👤 Add new user.

        Args:
            username (str): Username.
            password (str): Plain password.
            email (str): User email.
            role (str): Role type.

        Returns:
            str: Result message.
        """
        try:
            if not (username.isalnum() and "@" in email and "." in email):
                return "Invalid username or email."

            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            if role in {"admin", "kitchen_staff", "customer_support"}:
                self.cursor.execute("INSERT INTO staff (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
            else:
                self.cursor.execute("INSERT INTO customers (username, password_hash, email) VALUES (?, ?, ?)", (username, password_hash, email))

            self.connection.commit()
            return f"User {username} added."
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Error adding user"})
            return f"Error: {e}"

    def verify_user(self, username: str, password: str) -> Optional[str]:
        """🔐 Verify credentials and get role.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            Optional[str]: User role or None if invalid.
        """
        try:
            if not username.isalnum():
                return None

            self.cursor.execute("SELECT password_hash, role FROM staff WHERE username = ?", (username,))
            row = self.cursor.fetchone()
            if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
                return row["role"]

            self.cursor.execute("SELECT password_hash FROM customers WHERE username = ?", (username,))
            row = self.cursor.fetchone()
            if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
                return "customer"

            return None
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Error verifying user"})
            return None

    def check_existing_user(self, username, email):
        """✅ Check if the username OR email already exists in the database."""
        query = "SELECT * FROM customers WHERE username = ? OR email = ?"
        self.cursor.execute(query, (username, email))
        return self.cursor.fetchone()

    def close_connection(self):
        """🔒 Close SQLite connection."""
        try:
            self.connection.close()
            logger.info("🔐 Database connection closed")
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "❌ Error closing connection"})