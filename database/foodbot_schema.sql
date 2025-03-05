-- ✅ Switch to the database
USE foodbot;

-- ✅ Create the menu table to store food items and their prices
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each menu item
    name VARCHAR(100) UNIQUE NOT NULL,  -- Item name (must be unique and cannot be null)
    price DECIMAL(10,2) NOT NULL        -- Price of the item (up to two decimal places)
);

-- ✅ Create the orders table to store customer orders
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique order ID (auto-increment)
    user_id VARCHAR(255),                -- User identifier (session ID or user reference)
    items TEXT NOT NULL,                 -- Stores ordered items in JSON format (e.g., {"burger": 2, "pizza": 1})
    total_price DECIMAL(10,2) NOT NULL,  -- Total price of the order
    status ENUM('Pending', 'In Process', 'Completed') DEFAULT 'Pending'  -- Order status with default value as 'Pending'
);

-- ✅ Insert menu items into the menu table
INSERT INTO menu (name, price) VALUES
('Cheese Burger', 5.99),
('Chicken Burger', 6.99),
('Veggie Burger', 5.49),
('Pepperoni Pizza', 12.99),
('Margherita Pizza', 11.49),
('BBQ Chicken Pizza', 13.99),
('Grilled Chicken Sandwich', 7.99),
('Club Sandwich', 6.99),
('Spaghetti Carbonara', 9.99),
('Fettuccine Alfredo', 10.49),
('Tandoori Chicken', 11.99),
('Butter Chicken', 12.49),
('Beef Steak', 15.99),
('Chicken Biryani', 8.99),
('Mutton Biryani', 10.99),
('Prawn Curry', 13.49),
('Fish and Chips', 9.49),
('French Fries', 3.99),
('Garlic Bread', 4.49),
('Chocolate Brownie', 5.49),
('Vanilla Ice Cream', 3.99),
('Strawberry Shake', 4.99),
('Mango Smoothie', 5.49),
('Coca-Cola', 2.49),
('Pepsi', 2.49),
('Fresh Orange Juice', 4.99);

-- ✅ Insert sample orders into the orders table
INSERT INTO orders (user_id, items, total_price, status) VALUES
('user_001', '{"Cheese Burger": 2, "French Fries": 1, "Coca-Cola": 1}', 17.46, 'Pending'),
('user_002', '{"Pepperoni Pizza": 1, "Garlic Bread": 1, "Pepsi": 1}', 19.97, 'In Process'),
('user_003', '{"Chicken Biryani": 2, "Mango Smoothie": 1}', 23.47, 'Completed'),
('user_004', '{"Club Sandwich": 1, "Strawberry Shake": 1}', 11.98, 'Pending'),
('user_005', '{"Beef Steak": 1, "Fresh Orange Juice": 1}', 20.98, 'In Process');

-- ✅ Add time and date columns to track order placement time
ALTER TABLE orders ADD COLUMN time TIME;  -- Stores order placement time
ALTER TABLE orders ADD COLUMN date DATE;  -- Stores order placement date

-- ✅ Remove the user_id column (if not needed)
ALTER TABLE orders DROP COLUMN user_id;

-- ✅ Retrieve all menu items where the name contains "Pizza"
SELECT * FROM menu WHERE name="Pizza";

-- ✅ Retrieve all orders
SELECT * FROM orders;

-- ✅ Retrieve all menu items
SELECT * FROM menu;

-- ✅ Insert a new order with current date and time
INSERT INTO orders (id, items, total_price, status, date, time) 
VALUES (27, '{"Pepsi": 2, "Coca-Cola": 2}', 9.96, "Pending", CURDATE(), CURTIME());

-- ✅ Modify the status column to allow longer status values
ALTER TABLE orders MODIFY COLUMN status VARCHAR(15);

-- ✅ Show the structure of the orders table
SHOW COLUMNS FROM orders;

-- ✅ Update an order's status to 'Canceled' based on order ID
UPDATE orders SET status = "Canceled" WHERE id = 29;

-- ✅ Retrieve all orders to verify the update
SELECT * FROM orders;
