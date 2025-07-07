-- -- DineMate Database Schema 🗄️

-- -- Create the menu table to store food items and their prices
-- CREATE TABLE IF NOT EXISTS menu (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT UNIQUE NOT NULL,
--     price REAL NOT NULL
-- );

-- -- Create the orders table to store customer orders
-- CREATE TABLE IF NOT EXISTS orders (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     items TEXT NOT NULL,
--     total_price REAL NOT NULL,
--     status TEXT CHECK(status IN ('Pending', 'Preparing', 'In Process', 'Ready', 'Completed', 'Delivered', 'Canceled')) DEFAULT 'Pending',
--     date TEXT DEFAULT (DATE('now')),
--     time TEXT DEFAULT (TIME('now'))
-- );

-- -- Create indexes for faster queries
-- CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
-- CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(date);

-- -- Create staff table
-- CREATE TABLE IF NOT EXISTS staff (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL,
--     role TEXT CHECK(role IN ('admin', 'kitchen_staff', 'customer_support')) NOT NULL,
--     is_staff BOOLEAN DEFAULT TRUE
-- );

-- -- Create customers table
-- CREATE TABLE IF NOT EXISTS customers (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL,
--     email TEXT UNIQUE,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );