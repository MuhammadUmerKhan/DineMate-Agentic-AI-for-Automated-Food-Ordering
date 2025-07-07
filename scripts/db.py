"""
# DineMate Database Operations 🗄️

This module handles all database interactions for DineMate using SQLite.

Dependencies:
- sqlite3: For database operations 🗄️.
- datetime: For timestamp handling 🕒.
- json: For JSON serialization 🗃️.
- bcrypt: For password hashing 🔒.
- pandas: For DataFrame operations 📊.
- logger: For structured logging 📜.
- config: For database configuration ⚙️.
"""

import sqlite3, datetime, json, bcrypt, pandas as pd
from typing import Dict, Optional, List
from scripts.logger import get_logger
from scripts.config import DB_PATH

# Configure logger
logger = get_logger(__name__)

class Database:
    def __init__(self, db_path=DB_PATH):
        """🗄️ Initialize and connect to the SQLite database.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        try:
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.info({"message": "Connected to SQLite database successfully"})
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "Database connection failed"})
            raise

    def fetch_order_data(self, status: Optional[str] = "Delivered") -> pd.DataFrame:
        """📦 Fetch order data as a pandas DataFrame, filtered by status.

        Args:
            status (Optional[str]): Order status to filter by (e.g., 'Delivered', 'Canceled'). 
                                   If None or 'All', fetch all orders. Defaults to 'Delivered'.

        Returns:
            pd.DataFrame: DataFrame containing order data (id, items, total_price, status, date, time).
        """
        logger.info({"status": status, "message": "Fetching order data for analytics"})
        try:
            if status and status != "All":
                query = "SELECT id, items, total_price, status, date, time FROM orders WHERE status = ?"
                df = pd.read_sql_query(query, self.connection, params=(status,))
            else:
                query = "SELECT id, items, total_price, status, date, time FROM orders"
                df = pd.read_sql_query(query, self.connection)
            logger.info({"rows": len(df), "status": status, "message": "Order data fetched successfully"})
            return df
        except sqlite3.Error as e:
            logger.error({"error": str(e), "status": status, "message": "Failed to fetch order data"})
            return pd.DataFrame()
        except Exception as e:
            logger.error({"error": str(e), "status": status, "message": "Unexpected error fetching order data"})
            return pd.DataFrame()

    def load_menu(self):
        """🍽️ Fetch all menu items.

        Returns:
            List[Dict]: List of menu items or None if error.
        """
        try:
            self.cursor.execute("SELECT * FROM menu")
            menu = [dict(row) for row in self.cursor.fetchall()]
            logger.info({"count": len(menu), "message": "Fetched menu items"})
            return menu or None
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "Error fetching menu"})
            return None

    def get_max_id(self) -> int:
        """🔢 Fetch the maximum ID from the orders table.

        Returns:
            int: Next available order ID.
        """
        try:
            self.cursor.execute("SELECT MAX(id) FROM orders")
            result = self.cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            logger.info({"max_id": max_id, "message": "Fetched max order ID"})
            return max_id + 1
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "Error fetching max ID"})
            return 1

    def store_order_db(self, order_dict: Dict[str, int], price: float, status: str = "Pending") -> Optional[int]:
        """📦 Store the confirmed order in the database.

        Args:
            order_dict (Dict[str, int]): Order items and quantities.
            price (float): Total price.
            status (str): Order status.

        Returns:
            Optional[int]: Order ID or None if error.
        """
        try:
            order_json = json.dumps(order_dict)
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%I:%M:%S %p")
            order_id = self.get_max_id()
            self.cursor.execute(
                "INSERT INTO orders (id, items, total_price, status, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, order_json, price, status, date, time)
            )
            self.connection.commit()
            logger.info({"order_id": order_id, "message": "Order stored successfully"})
            return order_id
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "Error storing order"})
            return None

    def check_order_status_db(self, order_id: int) -> str:
        """🔍 Fetch order status and estimated delivery time.

        Args:
            order_id (int): Order ID.

        Returns:
            str: Status and delivery time or error message.
        """
        logger.info({"order_id": order_id, "message": "Checking order status"})
        try:
            self.cursor.execute("SELECT status, time, date FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                logger.warning({"order_id": order_id, "message": "No order found"})
                return f"No order found with ID {order_id}"

            order_status = result["status"]
            valid_statuses = ["Pending", "Preparing", "In Process", "Ready", "Completed", "Delivered", "Canceled"]
            if order_status not in valid_statuses:
                logger.error({"order_id": order_id, "status": order_status, "message": "Invalid order status"})
                return f"Invalid order status for ID {order_id}"

            if order_status in ["Canceled", "Delivered"]:
                logger.info({"order_id": order_id, "status": order_status, "message": "Order status retrieved"})
                return f"Order {order_id} is already {order_status.lower()}."

            order_datetime = datetime.datetime.strptime(
                f"{result['date']} {result['time']}", "%Y-%m-%d %I:%M:%S %p"
            )
            estimated_datetime = order_datetime + datetime.timedelta(minutes=40)
            estimated_time_str = estimated_datetime.strftime("%I:%M %p")
            current_datetime = datetime.datetime.now()

            if current_datetime > estimated_datetime:
                delay_minutes = int((current_datetime - estimated_datetime).total_seconds() / 60)
                return f"Order Status: {order_status}\nEstimated Delivery Time: {estimated_time_str} (delayed by ~{delay_minutes} minutes)"
            return f"Order Status: {order_status}\nEstimated Delivery Time: {estimated_time_str}"

        except (sqlite3.Error, ValueError) as e:
            logger.error({"error": str(e), "order_id": order_id, "message": "Error fetching order status"})
            return f"Error fetching order status: {e}"

    def cancel_order_after_confirmation(self, order_id: int) -> str:
        """❌ Cancel order if within 10 minutes.

        Args:
            order_id (int): Order ID.

        Returns:
            str: Confirmation or error message.
        """
        logger.info({"order_id": order_id, "message": "Checking cancellation"})
        try:
            self.cursor.execute("SELECT status, date, time FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                logger.warning({"order_id": order_id, "message": "No order found"})
                return f"No order found with ID {order_id}"

            order_status = result["status"]
            if order_status in ["Canceled", "Completed", "Delivered"]:
                logger.info({"order_id": order_id, "status": order_status, "message": "Order cannot be canceled"})
                return f"Order {order_id} is already {order_status.lower()} and cannot be canceled."

            order_datetime = datetime.datetime.strptime(
                f"{result['date']} {result['time']}", "%Y-%m-%d %I:%M:%S %p"
            )
            time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60
            if time_diff > 10:
                logger.warning({"order_id": order_id, "message": "Cannot cancel: past 10-minute window"})
                return "Cannot cancel order: past 10-minute window."

            self.cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Canceled", order_id))
            self.connection.commit()
            logger.info({"order_id": order_id, "message": "Order canceled successfully"})
            return f"Order {order_id} canceled successfully."

        except (sqlite3.Error, ValueError) as e:
            logger.error({"error": str(e), "order_id": order_id, "message": "Error canceling order"})
            return f"Error canceling order: {e}"

    def modify_order_after_confirmation(self, order_id: int, updated_items: Dict[str, int], new_total_price: float) -> str:
        """✏️ Modify order if within 10 minutes.

        Args:
            order_id (int): Order ID.
            updated_items (Dict[str, int]): Updated items and quantities.
            new_total_price (float): New total price.

        Returns:
            str: Confirmation or error message.
        """
        logger.info({"order_id": order_id, "message": "Checking modification"})
        try:
            if not updated_items:
                logger.warning({"order_id": order_id, "message": "No items provided"})
                return "No items provided in the updated order."

            # Validate items against menu
            menu = self.load_menu()
            menu_dict = {item["name"].lower(): float(item["price"]) for item in menu} if menu else {}
            for item in updated_items:
                if item.lower() not in menu_dict:
                    logger.warning({"order_id": order_id, "item": item, "message": "Invalid item"})
                    return f"Item {item} is not available in the menu."

            self.cursor.execute("SELECT status, date, time FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                logger.warning({"order_id": order_id, "message": "No order found"})
                return f"No order found with ID {order_id}"

            order_status = result["status"]
            if order_status not in ["Pending", "Preparing"]:
                logger.info({"order_id": order_id, "status": order_status, "message": "Order cannot be modified"})
                return f"Order {order_id} is {order_status.lower()} and cannot be modified."

            order_datetime = datetime.datetime.strptime(
                f"{result['date']} {result['time']}", "%Y-%m-%d %I:%M:%S %p"
            )
            time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60
            if time_diff > 10:
                logger.warning({"order_id": order_id, "message": "Cannot modify: past 10-minute window"})
                return "Cannot modify order: past 10-minute window."

            updated_items_json = json.dumps(updated_items)
            self.cursor.execute(
                "UPDATE orders SET items = ?, total_price = ? WHERE id = ?",
                (updated_items_json, new_total_price, order_id)
            )
            self.connection.commit()
            items_str = ", ".join(f"{item}: {qty}" for item, qty in updated_items.items())
            logger.info({"order_id": order_id, "items": items_str, "total_price": new_total_price, "message": "Order updated successfully"})
            return f"Order {order_id} updated successfully. Items: {items_str}, Total: ${new_total_price:.2f}"

        except (sqlite3.Error, ValueError) as e:
            logger.error({"error": str(e), "order_id": order_id, "message": "Error updating order"})
            return f"Error updating order: {e}"

    def get_order_by_id(self, order_id: int) -> Dict[str, any]:
        """🔍 Retrieve order details by ID.

        Args:
            order_id (int): Order ID.

        Returns:
            Dict[str, any]: Order details with eligibility message.
        """
        logger.info({"order_id": order_id, "message": "Fetching order details"})
        try:
            self.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = self.cursor.fetchone()
            if not order:
                logger.warning({"order_id": order_id, "message": "No order found"})
                return {"status": "error", "message": f"No order found with ID {order_id}"}

            order_dict = dict(order)
            items = json.loads(order_dict["items"])
            order_status = order_dict["status"]
            items_str = ", ".join(f"{item}: {quantity}" for item, quantity in items.items())
            details = {
                "order_id": order_dict["id"],
                "items": items,
                "total_price": order_dict["total_price"],
                "status": order_status,
                "message": f"Order {order_dict['id']}: {items_str}, Total: ${order_dict['total_price']:.2f}, Status: {order_status}"
            }

            if order_status == "Pending":
                order_datetime = datetime.datetime.strptime(
                    f"{order_dict['date']} {order_dict['time']}", "%Y-%m-%d %I:%M:%S %p"
                )
                time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60
                if time_diff <= 10:
                    remaining_minutes = int(10 - time_diff)
                    details["message"] += f"\nYou have {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''} to modify or cancel."
                else:
                    details["message"] += "\nCannot modify or cancel: past 10-minute window."
            else:
                details["message"] += f"\nCannot modify or cancel: order is {order_status.lower()}."

            logger.info({"order_id": order_id, "message": details["message"]})
            return details

        except (sqlite3.Error, json.JSONDecodeError, ValueError) as e:
            logger.error({"error": str(e), "order_id": order_id, "message": "Error fetching order"})
            return {"status": "error", "message": f"Error fetching order: {e}"}

    def add_user(self, username: str, password: str, email: str, role: str = "customer") -> str:
        """👤 Add a new user.

        Args:
            username (str): Username.
            password (str): Password.
            email (str): Email address.
            role (str): User role (default: customer).

        Returns:
            str: Success or error message.
        """
        try:
            if not (username.isalnum() and "@" in email and "." in email):
                logger.warning({"username": username, "email": email, "message": "Invalid username or email"})
                return "Invalid username or email format."
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            if role in ["admin", "kitchen_staff", "customer_support"]:
                self.cursor.execute(
                    "INSERT INTO staff (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
            else:
                self.cursor.execute(
                    "INSERT INTO customers (username, password_hash, email) VALUES (?, ?, ?)",
                    (username, password_hash, email)
                )
            self.connection.commit()
            logger.info({"username": username, "role": role, "message": "User added successfully"})
            return f"User {username} added successfully."
        except sqlite3.Error as e:
            logger.error({"error": str(e), "username": username, "message": "Error adding user"})
            return f"Error adding user: {e}"

    def verify_user(self, username: str, password: str) -> Optional[str]:
        """🔐 Verify user credentials.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            Optional[str]: Role if valid, None otherwise.
        """
        try:
            if not username.isalnum():
                logger.warning({"username": username, "message": "Invalid username format"})
                return None
            self.cursor.execute("SELECT password_hash, role FROM staff WHERE username = ?", (username,))
            staff_user = self.cursor.fetchone()
            if staff_user and bcrypt.checkpw(password.encode('utf-8'), staff_user["password_hash"].encode('utf-8')):
                logger.info({"username": username, "role": staff_user["role"], "message": "Staff user verified"})
                return staff_user["role"]

            self.cursor.execute("SELECT password_hash FROM customers WHERE username = ?", (username,))
            customer_user = self.cursor.fetchone()
            if customer_user and bcrypt.checkpw(password.encode('utf-8'), customer_user["password_hash"].encode('utf-8')):
                logger.info({"username": username, "message": "Customer user verified"})
                return "customer"
            
            logger.warning({"username": username, "message": "User verification failed"})
            return None
        except sqlite3.Error as e:
            logger.error({"error": str(e), "username": username, "message": "Error verifying user"})
            return None
        
    def close_connection(self):
        """🔒 Close the database connection."""
        try:
            self.connection.close()
            logger.info({"message": "Database connection closed"})
        except sqlite3.Error as e:
            logger.error({"error": str(e), "message": "Error closing database connection"})