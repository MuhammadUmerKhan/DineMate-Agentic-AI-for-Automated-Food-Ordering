import mysql.connector
import logging
from mysql.connector import Error
import datetime
import json
import datetime
from config import DB_CONFIG

# Configure logging
logging.basicConfig(filename="foodbot.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Database:
    def __init__(self):
        """Initialize and connect to the database."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            logging.info("Connected to the database successfully.")
        except Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def load_menu(self):
        """Fetch all menu items."""
        try:
            self.cursor.execute("SELECT * FROM menu;")
            return self.cursor.fetchall()
        except Error as e:
            logging.error(f"Error fetching menu: {e}")
            return None

    def get_max_id(self):
        """Fetch the maximum ID from the orders table."""
        try:
            self.cursor.execute("SELECT MAX(id) FROM orders;")
            result = self.cursor.fetchone()
            return int(result["MAX(id)"]) + 1 if result else 0
        except Error as e:
            logging.error(f"Error fetching max ID: {e}")
            return 0
        
    def store_order(self, user_id, order_dict, price, status):
        """✅ Stores the confirmed order in the database with date and time."""
        try:
            order_json = json.dumps(order_dict)  # Convert dict to JSON string
            sql_query = """
            INSERT INTO orders (id, items, total_price, status, date, time) 
            VALUES (%s, %s, %s, %s, CURDATE(), CURTIME());
            """
            values = (user_id, order_json, price, status)
            
            self.cursor.execute(sql_query, values)
            self.connection.commit()
            
            return f"✅ Order stored successfully for user {user_id}: {order_dict}"
        except Exception as e:
            return f"⚠ Error storing order: {e}"

    def check_order_status(self, order_id):
        """✅ Fetch the order status and estimated delivery time."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = %s;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()
            
            if not result:
                return f"⚠ No order found with ID {order_id}."
            
            order_status = result["status"]
            
            if order_status == "Canceled":
                return f"��� Order {order_id} is already canceled. You can re order items again"
            
            order_time = result["time"]  # Fetch stored time

            # Convert time to datetime and add 40 minutes
            order_time_obj = datetime.datetime.strptime(str(order_time), "%H:%M:%S")
            delivery_time_obj = order_time_obj + datetime.timedelta(minutes=40)
            estimated_delivery_time = delivery_time_obj.strftime("%I:%M %p")  # Format as HH:MM AM/PM
            
            return (f"📝 **Order Status:** {order_status}\n"
                    f"🚚 **Estimated Delivery Time:** {estimated_delivery_time} and you have 20 minutes to cancel the order.")
        
        except Exception as e:
            return f"⚠ Error fetching order status: {e}"

    def estimated_delivery_time(self, order_id):
        """✅ Returns estimated delivery time (40 minutes after placement)."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = %s;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()
            
            if not result:
                return f"⚠ No order found with ID {order_id}."
            
            order_status = result["status"]
            
            if order_status == "Canceled":
                return f"��� Order {order_id} is already canceled. You can re order items again"
            
            order_time = result["time"]  # Fetch stored time

            # ✅ Ensure order_time is of type `time`, not `timedelta`
            if isinstance(order_time, datetime.timedelta):
                total_seconds = order_time.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                order_time = datetime.time(hour=hours, minute=minutes)

            # ✅ Calculate estimated delivery time (40 minutes after order time)
            order_datetime = datetime.datetime.combine(datetime.date.today(), order_time)
            estimated_time = order_datetime + datetime.timedelta(minutes=40)
            
            return f"🚚 Your order is currently {order_status} and  will be delivered by **{estimated_time.strftime('%I:%M %p')}**."
                
        except Exception as e:
            return f"⚠ Error fetching order status: {e}"

    def cancel_order_after_confirmation(self, order_id):
        """✅ Cancels the order if it's within 20 minutes of placement."""
        try:
            sql_query = "SELECT status, time FROM orders WHERE id = %s;"
            self.cursor.execute(sql_query, (order_id,))
            result = self.cursor.fetchone()

            if not result:
                return f"⚠ No order found with ID {order_id}."

            order_status = result["status"]
            order_time = result["time"]

            # ✅ Ensure the order is not already canceled or completed
            if order_status in ["Canceled", "Completed"]:
                return f"⚠ Order {order_id} is already **{order_status}** and cannot be canceled."

            # ✅ Handle both `datetime.time` and `timedelta` return types from MySQL
            if isinstance(order_time, datetime.timedelta):
                # Convert `timedelta` to `time`
                seconds = order_time.total_seconds()
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                order_time = datetime.time(hour=hours, minute=minutes)

            # ✅ Combine with today's date to get full timestamp
            order_time_obj = datetime.datetime.combine(datetime.date.today(), order_time)
            current_time_obj = datetime.datetime.now()

            # ✅ Ensure order time is not in the future (data consistency check)
            if order_time_obj > current_time_obj:
                return "⚠ **Order time is incorrect in the database. Please contact support.**"

            # ✅ Calculate time difference in minutes
            time_diff = (current_time_obj - order_time_obj).total_seconds() / 60  

            if time_diff > 20:
                return "⚠ **Your order cannot be canceled now. It has been more than 20 minutes.**"

            # ✅ If within 20 minutes, cancel the order
            update_query = "UPDATE orders SET status = %s WHERE id = %s;"
            self.cursor.execute(update_query, ("Canceled", order_id))
            self.connection.commit()

            return f"✅ **Order {order_id} has been successfully canceled.**"

        except Exception as e:
            return f"⚠ Error canceling order: {e}"
    
    def modify_order_after_confirmation(self, order_id, updated_items_json, new_total_price):
        """✅ Replace the existing order with new items and updated price."""
        try:
            # ✅ Update order with new items and new total price
            update_query = "UPDATE orders SET items = %s, total_price = %s WHERE id = %s;"
            self.cursor.execute(update_query, (updated_items_json, new_total_price, order_id))
            self.connection.commit()

            return (f"✅ **Order {order_id} has been successfully updated.**\n"
                    f"🛒 **Updated Order:** {updated_items_json}\n"
                    f"💰 **New Total Price: ${new_total_price:.2f}**")

        except Exception as e:
            return f"⚠ Error updating order: {e}"


    def close_connection(self):
        """✅ Close database connection."""
        self.connection.close()

# Example Usage
if __name__ == "__main__":
    db = Database()
    # print(db.fetch_menu())  # Fetch menu
    # db.place_order("user_007", '{"Butter Chicken": 1, "Naan": 2}', 14.99)  # Place order
    # print(db.get_order_status("user_007"))  # Check order status
    # db.update_order_status("user_007", "Completed")  # Update order status
    # db.close_connection()
    # print(db.get_max_id())
    print(db.store_order(33, {"Pepsi": 3}, 3, "Pending"))
    # print(db.get_order_status(17))
    # print(db.estimated_delivery_time(30))
    # print(db.modify_order_after_confirmation(33, {"Pepsi": 3}))