import sqlite3, datetime, json, bcrypt
from scripts.logger import get_logger
from scripts.config import DB_PATH

# Configure logger
logger = get_logger(__name__)

class Database:
    def __init__(self, db_path=DB_PATH):
        """Initialize and connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.info("Connected to SQLite database successfully")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def load_menu(self):
        """Fetch all menu items."""
        try:
            self.cursor.execute("SELECT * FROM menu")
            menu = [dict(row) for row in self.cursor.fetchall()]
            logger.info(f"Fetched {len(menu)} menu items")
            return menu or None
        except sqlite3.Error as e:
            logger.error(f"Error fetching menu: {e}")
            return None

    def get_max_id(self):
        """✅ Fetch the maximum ID from the orders table."""
        try:
            self.cursor.execute("SELECT MAX(id) FROM orders;")
            result = self.cursor.fetchone()
            return int(result["MAX(id)"]) + 1 if result and result["MAX(id)"] else 1  # ✅ Default to 1
        except sqlite3.Error as e:
            logger.error(f"⚠ Error fetching max ID: {e}")
            return 1  # ✅ Default to 1

    def store_order_db(self, order_dict, price, status="Pending"):
        """Store the confirmed order in the database with date and time."""
        try:
            order_json = json.dumps(order_dict)
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%I:%M:%S %p")
            order_id = self.get_max_id()
            
            sql_query = """
                INSERT INTO orders (id, items, total_price, status, date, time)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (order_id, order_json, price, status, date, time)
            
            self.cursor.execute(sql_query, values)
            self.connection.commit()
            logger.info(f"Order {order_id} stored successfully")
            return order_id
        except sqlite3.Error as e:
            logger.error(f"Error storing order: {e}")
            return None

    def check_order_status_db(self, order_id):
        logger.info(f"Checking status for order ID: {order_id}")
        try:
            self.cursor.execute("SELECT status, time, date FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                logger.warning(f"No order found with ID {order_id}")
                return f"No order found with ID {order_id}"

            order_status = result["status"]
            valid_statuses = ['Pending', 'Preparing', 'In Process', 'Ready', 'Completed', 'Delivered', 'Canceled']
            if order_status not in valid_statuses:
                logger.error(f"Invalid status '{order_status}' for order {order_id}")
                return f"Invalid order status for ID {order_id}"

            if order_status == "Canceled":
                logger.info(f"Order {order_id} is Canceled")
                return f"Order {order_id} is already canceled. Please reorder."

            if order_status == "Delivered":
                logger.info(f"Order {order_id} is Delivered")
                return f"Order {order_id} has already been delivered. We hope you enjoyed our service!"

            # Combine date and time for accurate datetime calculation
            order_datetime = datetime.datetime.strptime(
                f"{result['date']} {result['time']}", "%Y-%m-%d %I:%M:%S %p"
            )
            estimated_datetime = order_datetime + datetime.timedelta(minutes=40)
            estimated_time_str = estimated_datetime.strftime("%I:%M %p")
            current_datetime = datetime.datetime.now()

            logger.info(f"Order {order_id} status: {order_status}, estimated delivery: {estimated_time_str}")

            if order_status == "Completed":
                return f"Order Status: {order_status}\nYour order has been completed."

            # For Pending, Preparing, In Process, Ready: check if estimated time has passed
            if current_datetime > estimated_datetime:
                delay_minutes = int((current_datetime - estimated_datetime).total_seconds() / 60)
                return (f"Order Status: {order_status}\n"
                        f"Estimated Delivery Time: {estimated_time_str} (delayed by ~{delay_minutes} minutes)")
            return f"Order Status: {order_status}\nEstimated Delivery Time: {estimated_time_str}"

        except sqlite3.Error as e:
            logger.error(f"Error fetching order status for ID {order_id}: {e}")
            return f"Error fetching order status: {e}"
        except ValueError as e:
            logger.error(f"Error parsing datetime for order {order_id}: {e}")
            return f"Error processing order time: {e}"

    def cancel_order_after_confirmation(self, order_id):
        """Cancel the order if within 10 minutes of placement.
        :param order_id: The ID of the order to cancel.
        :return: Confirmation or error message.
        """
        logger.info(f"Checking cancellation for order ID: {order_id}")
        try:
            self.cursor.execute("SELECT status, date, time FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                logger.warning(f"No order found with ID {order_id}")
                return f"No order found with ID {order_id}"

            order_status = result["status"]
            non_cancelable_statuses = ["Canceled", "Completed", "Delivered"]
            if order_status in non_cancelable_statuses:
                logger.info(f"Order {order_id} is already {order_status}")
                return f"Order {order_id} is already {order_status} and cannot be canceled."

            order_datetime = datetime.datetime.strptime(
                f"{result['date']} {result['time']}", "%Y-%m-%d %I:%M:%S %p"
            )
            time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60

            if time_diff > 10:
                logger.warning(f"Order {order_id} cannot be canceled: past 10-minute window")
                return "Your order cannot be canceled now. It has been more than 10 minutes."

            self.cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Canceled", order_id))
            self.connection.commit()
            logger.info(f"Order {order_id} canceled successfully")
            return f"Order {order_id} has been successfully canceled."

        except sqlite3.Error as e:
            logger.error(f"Error canceling order {order_id}: {e}")
            return f"Error canceling order: {e}"
        except ValueError as e:
            logger.error(f"Error parsing datetime for order {order_id}: {e}")
            return f"Error processing order time: {e}"

    def modify_order_after_confirmation(self, order_id, updated_items_json, new_total_price):
        """Replace the existing order with new items and updated price if within 10 minutes.
        :param order_id: The ID of the order to modify.
        :param updated_items_json: JSON string of updated items (e.g., '{"pizza": 2, "cola": 1}').
        :param new_total_price: New total price (float).
        :return: Confirmation or error message.
        """
        logger.info(f"Checking modification for order ID: {order_id}")
        try:
            # Validate JSON input
            try:
                items = json.loads(updated_items_json)
                if not items:
                    logger.warning(f"No items provided for order {order_id}")
                    return "No items provided in the updated order."
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON for order {order_id}: {e}")
                return "Invalid order items format. Please provide valid JSON."

            # Check order exists and status
            self.cursor.execute("SELECT status, date, time FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                logger.warning(f"No order found with ID {order_id}")
                return f"No order found with ID {order_id}"

            order_status = result["status"]
            modifiable_statuses = ["Pending", "Preparing"]
            if order_status not in modifiable_statuses:
                logger.info(f"Order {order_id} is {order_status} and cannot be modified")
                return f"Order {order_id} is {order_status} and cannot be modified."

            # Check 10-minute window
            order_datetime = datetime.datetime.strptime(
                f"{result['date']} {result['time']}", "%Y-%m-%d %I:%M:%S %p"
            )
            time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60
            if time_diff > 10:
                logger.warning(f"Order {order_id} cannot be modified: past 10-minute window")
                return "Your order cannot be modified now. It has been more than 10 minutes."

            # Update order
            self.cursor.execute(
                "UPDATE orders SET items = ?, total_price = ? WHERE id = ?",
                (updated_items_json, new_total_price, order_id)
            )
            self.connection.commit()
            logger.info(f"Order {order_id} updated successfully")
            return (f"Order {order_id} has been successfully updated.\n"
                    f"Updated Order: {updated_items_json}\nNew Total Price: ${new_total_price:.2f}")

        except sqlite3.Error as e:
            logger.error(f"Error updating order {order_id}: {e}")
            return f"Error updating order: {e}"
        except ValueError as e:
            logger.error(f"Error parsing datetime for order {order_id}: {e}")
            return f"Error processing order time: {e}"

    def get_order_by_id(self, order_id):
        """Retrieve order details by ID, including modification eligibility.
        :param order_id: The ID of the order to retrieve.
        :return: Dictionary with order details, status, and eligibility message.
        """
        logger.info(f"Fetching details for order ID: {order_id}")
        try:
            self.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = self.cursor.fetchone()
            if not order:
                logger.warning(f"No order found with ID {order_id}")
                return {"status": "error", "message": f"No order found with ID {order_id}"}

            order_dict = dict(order)
            items = json.loads(order_dict["items"])
            order_status = order_dict["status"]

            # Format items for display
            items_str = ", ".join(f"{item}: {quantity}" for item, quantity in items.items())
            details = {
                "order_id": order_dict["id"],
                "items": items,
                "total_price": order_dict["total_price"],
                "status": order_status,
                "message": f"Order Details: {items_str}, Total Price: ${order_dict['total_price']:.2f}, Status: {order_status}"
            }

            # Check 10-minute window for Pending orders
            if order_status == "Pending":
                order_datetime = datetime.datetime.strptime(
                    f"{order_dict['date']} {order_dict['time']}", "%Y-%m-%d %I:%M:%S %p"
                )
                time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60
                if time_diff <= 10:
                    remaining_minutes = int(10 - time_diff)
                    details["message"] += f"\nYou have {remaining_minutes} minutes left to modify or cancel this order."
                else:
                    details["message"] += "\nYou can no longer modify or cancel this order (past 10-minute window)."
            else:
                details["message"] += "\nYou can no longer modify or cancel this order."

            logger.info(f"Fetched order {order_id}: {details['message']}")
            return details

        except sqlite3.Error as e:
            logger.error(f"Error fetching order {order_id}: {e}")
            return {"status": "error", "message": f"Error fetching order: {e}"}
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Error processing order {order_id}: {e}")
            return {"status": "error", "message": f"Error processing order details: {e}"}
        
    def add_user(self, username, password, email, role="customer"):
        """Add a new user (staff or customer)."""
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            if role in ["admin", "kitchen_staff", "customer_support"]:
                self.cursor.execute("INSERT INTO staff (username, password_hash, role) VALUES (?, ?, ?)", 
                                  (username, password_hash, role))
            else:
                self.cursor.execute("INSERT INTO customers (username, password_hash, email) VALUES (?, ?, ?)", 
                                  (username, password_hash, email))
            self.connection.commit()
            logger.info(f"User {username} added successfully as {role}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error adding user {username}: {e}")
            return f"Error adding user: {e}"

    def verify_user(self, username, password):
        """Verify user credentials and return role if valid."""
        try:
            self.cursor.execute("SELECT password_hash, role FROM staff WHERE username = ?", (username,))
            staff_user = self.cursor.fetchone()
            if staff_user and bcrypt.checkpw(password.encode('utf-8'), staff_user["password_hash"].encode('utf-8')):
                logger.info(f"User {username} verified as staff: {staff_user['role']}")
                return staff_user["role"]

            self.cursor.execute("SELECT password_hash FROM customers WHERE username = ?", (username,))
            customer_user = self.cursor.fetchone()
            if customer_user and bcrypt.checkpw(password.encode('utf-8'), customer_user["password_hash"].encode('utf-8')):
                logger.info(f"User {username} verified as customer")
                return "customer"
            
            logger.warning(f"User {username} verification failed")
            return None
        except sqlite3.Error as e:
            logger.error(f"Error verifying user {username}: {e}")
            return None

    def check_existing_user(self, username, email):
        """Check if username or email already exists."""
        try:
            self.cursor.execute("SELECT * FROM customers WHERE username = ? OR email = ?", (username, email))
            user = self.cursor.fetchone()
            if user:
                logger.info(f"Existing user found: username={username}, email={email}")
            return user
        except sqlite3.Error as e:
            logger.error(f"Error checking existing user {username}: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        try:
            self.connection.close()
            logger.info("Database connection closed")
        except sqlite3.Error as e:
            logger.error(f"Error closing database connection: {e}")