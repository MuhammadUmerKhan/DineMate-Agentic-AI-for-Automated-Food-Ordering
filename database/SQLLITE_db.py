import sqlite3
import logging
import datetime
import json
import bcrypt
from config import *
import pandas as pd

# ✅ Configure logging
logging.basicConfig(filename="foodbot.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Database:
    def __init__(self, db_path=DB_PATH):
        """✅ Initialize and connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # ✅ Enables dictionary-like row access
            self.cursor = self.connection.cursor()
            logging.info("✅ Connected to the SQLite database successfully.")
        except sqlite3.Error as e:
            logging.error(f"⚠ Database connection failed: {e}")
            raise

    def load_menu(self):
        """✅ Fetch all menu items."""
        try:
            self.cursor.execute("SELECT * FROM menu;")
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"⚠ Error fetching menu: {e}")
            return None

    def get_max_id(self):
        """✅ Fetch the maximum ID from the orders table."""
        try:
            self.cursor.execute("SELECT MAX(id) FROM orders;")
            result = self.cursor.fetchone()
            return int(result["MAX(id)"]) + 1 if result and result["MAX(id)"] else 1  # ✅ Default to 1
        except sqlite3.Error as e:
            logging.error(f"⚠ Error fetching max ID: {e}")
            return 1  # ✅ Default to 1

    def store_order(self, order_dict, price, status):
        """✅ Stores the confirmed order in the database with date and time."""
        try:
            order_json = json.dumps(order_dict)  # ✅ Convert dict to JSON string
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")  # ✅ YYYY-MM-DD format
            time = now.strftime("%I:%M:%S %p")  # ✅ 12-hour format with AM/PM
            
            sql_query = """
            INSERT INTO orders (items, total_price, status, date, time) 
            VALUES (?, ?, ?, ?, ?);
            """
            values = (order_json, price, status, date, time)
            
            self.cursor.execute(sql_query, values)
            self.connection.commit()
            
            return f"✅ Order stored successfully: {order_dict}"
        except sqlite3.Error as e:
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
                return f"⚠ Order {order_id} is already canceled. Please reorder."

            order_time = datetime.datetime.strptime(result["time"], "%I:%M:%S %p")
            estimated_delivery_time = (order_time + datetime.timedelta(minutes=40)).strftime("%I:%M %p")
            
            return (f"📝 **Order Status:** {order_status}\n"
                    f"🚚 **Estimated Delivery Time:** {estimated_delivery_time}\n"
                    f"⏳ You have 10 minutes to cancel your order.")
        
        except sqlite3.Error as e:
            return f"⚠ Error fetching order status: {e}"

    def estimated_delivery_time(self, order_id):
        """✅ Returns estimated delivery time (40 minutes after placement)."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = ?;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()
            
            if not result:
                return f"⚠ No order found with ID {order_id}."
            
            order_status = result["status"]
            if order_status == "Canceled":
                return f"⚠ Order {order_id} is already canceled. Please reorder."

            order_time = datetime.datetime.strptime(result["time"], "%I:%M:%S %p")
            estimated_time = (order_time + datetime.timedelta(minutes=40)).strftime("%I:%M %p")
            
            return f"🚚 Your order is currently {order_status} and will be delivered by **{estimated_time}**."
                
        except sqlite3.Error as e:
            return f"⚠ Error fetching estimated delivery time: {e}"

    def cancel_order_after_confirmation(self, order_id):
        """✅ Cancels the order if it's within 10 minutes of placement."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = ?;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()

            if not result:
                return f"⚠ No order found with ID {order_id}."

            order_status = result["status"]
            if order_status in ["Canceled", "Completed"]:
                return f"⚠ Order {order_id} is already **{order_status}** and cannot be canceled."

            order_time = datetime.datetime.strptime(result["time"], "%I:%M:%S %p")
            time_diff = (datetime.datetime.now() - order_time).total_seconds() / 60  # ✅ Minutes

            if time_diff > 10:
                return "⚠ **Your order cannot be canceled now. It has been more than 10 minutes.**"

            update_query = "UPDATE orders SET status = ? WHERE id = ?;"
            self.cursor.execute(update_query, ("Canceled", order_id))
            self.connection.commit()

            return f"✅ **Order {order_id} has been successfully canceled.**"

        except sqlite3.Error as e:
            return f"⚠ Error canceling order: {e}"
    
    def modify_order_after_confirmation(self, order_id, updated_items_json, new_total_price):
        """✅ Replace the existing order with new items and updated price."""
        try:
            # ✅ Update order with new items and new total price
            update_query = "UPDATE orders SET items = ?, total_price = ? WHERE id = ?;"
            self.cursor.execute(update_query, (updated_items_json, new_total_price, order_id))
            self.connection.commit()

            return (f"✅ **Order {order_id} has been successfully updated.**\n"
                    f"🛒 **Updated Order:** {updated_items_json}\n"
                    f"💰 **New Total Price: ${new_total_price:.2f}**")

        except Exception as e:
            return f"⚠ Error updating order: {e}"

    def add_user(self, username, password, email, role="customer"):
        """✅ Add a new user (either staff or customer)."""
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if role in ["admin", "kitchen_staff", "customer_support"]:
                query = "INSERT INTO staff (username, password_hash, role) VALUES (?, ?, ?)"
                self.cursor.execute(query, (username, password_hash, role))
            else:
                query = "INSERT INTO customers (username, password_hash, email) VALUES (?, ?, ?)"
                self.cursor.execute(query, (username, password_hash, email))

            self.connection.commit()
            return True  

        except sqlite3.Error as e:
            return f"⚠ Error adding user: {e}"

    def verify_user(self, username, password):
        """✅ Verify user credentials and return role if valid."""
        query_staff = "SELECT password_hash, role FROM staff WHERE username = ?"
        self.cursor.execute(query_staff, (username,))
        staff_user = self.cursor.fetchone()

        if staff_user and bcrypt.checkpw(password.encode('utf-8'), staff_user["password_hash"].encode('utf-8')):
            return staff_user["role"]

        query_customer = "SELECT password_hash FROM customers WHERE username = ?"
        self.cursor.execute(query_customer, (username,))
        customer_user = self.cursor.fetchone()

        if customer_user and bcrypt.checkpw(password.encode('utf-8'), customer_user["password_hash"].encode('utf-8')):
            return "customer"
        
        return None  

    def check_existing_user(self, username, email):
        """✅ Check if the username OR email already exists in the database."""
        query = "SELECT * FROM customers WHERE username = ? OR email = ?"
        self.cursor.execute(query, (username, email))
        existing_user = self.cursor.fetchone()
        return existing_user  # Returns user if found, else None
    def fetch_order_data(self):
        """Fetch order data from the database and return it as a DataFrame."""
        try:
            query = "SELECT * FROM orders WHERE status = ?;"
            df = pd.read_sql(query, self.connection, params=("Delivered",))  # ✅ Correct parameter passing
            return df
        except sqlite3.Error as e:
            logging.error(f"⚠ Error fetching order data: {e}")
            return pd.DataFrame()  # Return empty DataFrame on failure
    def close_connection(self):
        """✅ Close the database connection."""
        self.connection.close()
        
    def get_order_by_id(self, order_id):
        """✅ Retrieve order details by ID."""
        try:
            conn = self.connection
            cursor = conn.cursor()
            
            # ✅ Debug: Print query execution log
            logging.info(f"🔍 Fetching order with ID: {order_id}")

            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = cursor.fetchone()

            if not order:
                logging.warning(f"⚠ No order found in database with ID {order_id}.")
                return None
            
            # ✅ Get column names dynamically
            column_names = [desc[0] for desc in cursor.description]
            order_dict = dict(zip(column_names, order))
            
            return order_dict

        except sqlite3.Error as e:
            logging.error(f"⚠ Error fetching order by ID: {e}")
            return None

# ✅ Example Usage
if __name__ == "__main__":
    db = Database()
    # print(db.load_menu())  # Fetch menu
    # print(db.get_max_id())
    # print(db.add_user("admin", "admin123", "admin"))
    # print(db.add_user("chef", "chef123", "kitchen_staff", "kitchen_staff"))
    # print(db.add_user("support", "support123", "customer_support", "customer_support"))
    # print(db.verify_user("admin", "admin123"))
    # print(db.verify_user("chef", "chef123"))
    # print(db.verify_user("support", "support123"))
    # print(db.add_user("umer", "umer123", "muhammadumerk546@gmail.com"))
    # print(db.verify_user("umer", "umer123"))