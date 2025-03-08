import sqlite3
import logging
import json
import bcrypt
import datetime
# from config import *

# Configure logging
logging.basicConfig(filename="foodbot.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Database:
    def __init__(self):
        """✅ Initialize and connect to the SQLite database."""
        try:
            db_path = "../sqllite3_db/foodbot.db"
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enables dict-like row access
            self.cursor = self.connection.cursor()
            logging.info("Connected to the SQLite database successfully.")
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def load_menu(self):
        """✅ Fetch all menu items."""
        try:
            self.cursor.execute("SELECT * FROM menu;")
            return [dict(row) for row in self.cursor.fetchall()]  # Convert rows to dict
        except Exception as e:
            logging.error(f"Error fetching menu: {e}")
            return None

    def get_max_id(self):
        """✅ Fetch the maximum order ID."""
        try:
            self.cursor.execute("SELECT MAX(id) FROM orders;")
            result = self.cursor.fetchone()
            return int(result["MAX(id)"]) + 1 if result["MAX(id)"] else 1  # Default to 1
        except Exception as e:
            logging.error(f"Error fetching max ID: {e}")
            return 1

    def store_order(self, order_dict, price, status="Pending"):
        """✅ Store a confirmed order with the correct date and time."""
        try:
            order_json = json.dumps(order_dict)  # Convert dict to JSON
            current_date = datetime.date.today().strftime("%Y-%m-%d")  # YYYY-MM-DD
            current_time = datetime.datetime.now().strftime("%H:%M:%S")  # HH:MM:SS
            
            sql_query = """
            INSERT INTO orders (items, total_price, status, date, time) 
            VALUES (?, ?, ?, ?, ?);
            """
            self.cursor.execute(sql_query, (order_json, price, status, current_date, current_time))
            self.connection.commit()
            return "✅ Order stored successfully!"
        except Exception as e:
            return f"⚠ Error storing order: {e}"

    def check_order_status(self, order_id):
        """✅ Fetch the order status and estimated delivery time."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = ?;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()
            
            if not result:
                return f"⚠ No order found with ID {order_id}."

            order_status = result["status"]

            if order_status == "Canceled":
                return f"❌ Order {order_id} is already canceled. Please reorder."

            order_time = result["time"]
            order_time_obj = datetime.datetime.strptime(order_time, "%H:%M:%S")
            estimated_time = order_time_obj + datetime.timedelta(minutes=40)

            return (f"📝 **Order Status:** {order_status}\n"
                    f"🚚 **Estimated Delivery:** {estimated_time.strftime('%I:%M %p')}")
        except Exception as e:
            return f"⚠ Error fetching order status: {e}"

    def cancel_order(self, order_id):
        """✅ Cancel an order if it's within 20 minutes of placement."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = ?;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()

            if not result:
                return f"⚠ No order found with ID {order_id}."

            if result["status"] in ["Canceled", "Completed"]:
                return f"⚠ Order {order_id} is already **{result['status']}**."

            order_time = result["time"]
            order_time_obj = datetime.datetime.strptime(order_time, "%H:%M:%S")
            current_time_obj = datetime.datetime.now()
            time_diff = (current_time_obj - order_time_obj).total_seconds() / 60

            if time_diff > 10:
                return "⚠ Order cannot be canceled after 20 minutes."

            self.cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Canceled", order_id))
            self.connection.commit()
            return f"✅ Order {order_id} has been successfully canceled."
        except Exception as e:
            return f"⚠ Error canceling order: {e}"

    def modify_order(self, order_id, updated_items, new_total_price):
        """✅ Modify an existing order after confirmation."""
        try:
            updated_items_json = json.dumps(updated_items)
            sql_query = "UPDATE orders SET items = ?, total_price = ? WHERE id = ?"
            self.cursor.execute(sql_query, (updated_items_json, new_total_price, order_id))
            self.connection.commit()
            return f"✅ Order {order_id} has been updated successfully."
        except Exception as e:
            return f"⚠ Error updating order: {e}"

    def add_user(self, username, password, email, role="customer"):
        """✅ Add a new user (customer or staff)."""
        try:
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            if role in ["admin", "kitchen_staff", "customer_support"]:
                sql_query = "INSERT INTO staff (username, password_hash, role) VALUES (?, ?, ?)"
                self.cursor.execute(sql_query, (username, password_hash, role))
            else:
                sql_query = "INSERT INTO customers (username, password_hash, email) VALUES (?, ?, ?)"
                self.cursor.execute(sql_query, (username, password_hash, email))

            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f"⚠ Error adding user: {e}")
            return False

    def verify_user(self, username, password):
        """✅ Verify user credentials and return role."""
        try:
            self.cursor.execute("SELECT password_hash, role FROM staff WHERE username = ?", (username,))
            staff_user = self.cursor.fetchone()

            if staff_user and bcrypt.checkpw(password.encode(), staff_user["password_hash"].encode()):
                return staff_user["role"]

            self.cursor.execute("SELECT password_hash FROM customers WHERE username = ?", (username,))
            customer_user = self.cursor.fetchone()

            if customer_user and bcrypt.checkpw(password.encode(), customer_user["password_hash"].encode()):
                return "customer"

            return None
        except Exception as e:
            logging.error(f"⚠ Error verifying user: {e}")
            return None

    def check_existing_user(self, username, email):
        """✅ Check if a user already exists."""
        try:
            self.cursor.execute("SELECT * FROM customers WHERE username = ? OR email = ?", (username, email))
            existing_user = self.cursor.fetchone()
            return existing_user is not None
        except Exception as e:
            logging.error(f"⚠ Error checking user: {e}")
            return False

    def close_connection(self):
        """✅ Close the database connection."""
        self.connection.close()
        logging.info("Database connection closed.")

# ✅ Example Usage
# if __name__ == "__main__":
    # db = Database()
    # print(db.load_menu())  # ✅ Fetch menu
    # print(db.store_order({"Pepsi": 3}, 3, "Pending"))  # ✅ Place order
    # print(db.check_order_status(7))  # ✅ Check order status
    # print(db.modify_order(7, {"Burger": 2}, 10))  # ✅ Modify order
    # print(db.cancel_order(7))  # ✅ Cancel order
    # print(db.add_user("admin", "admin123", "admin@gmail.com", "admin"))  # ✅ Add admin
    # print(db.verify_user("admin", "admin123"))  # ✅ Verify user
