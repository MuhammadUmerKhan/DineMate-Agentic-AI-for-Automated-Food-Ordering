# DineMate `database` Folder README 🗄️

This README provides an overview of the `database` folder in the **DineMate** project, an AI-powered food ordering system. The folder contains the SQLite database file and related schema scripts essential for storing and managing menu items, user data, and order details. All operations are optimized for performance and integrated with the app’s dark-themed UI (via `static/styles.css`).

## 📂 Folder Structure
The `database` folder houses the SQLite database file (`dinemate.db`) and any initialization scripts, ensuring persistent storage for menu, orders, and user information. It supports the app’s real-time functionality and analytics features.

## 📄 File Descriptions

- **🗃️ `dinemate.db`**
  - **Purpose**: The primary SQLite database file for DineMate.
  - **Key Features**:
    - 📋 Stores menu items (name, price) in the `menu` table.
    - 📦 Manages orders (ID, items, total price, status, time, date) in the `orders` table.
    - 👤 Handles user credentials (username, password hash, email, role) in the `users` table.
    - ⚡ Optimized with indexes on `status` and `date` for fast querying.
    - 📅 Contains 150+ orders spanning 2023–2025 with diverse statuses (Pending, Delivered, Canceled, etc.).
    - 🔒 Secured with structured logging for all database operations.
  - **Usage**: Initialized and populated via scripts or manual SQL commands; accessed by `scripts.db` module.

## 🎨 Theme Integration
- The database interacts with the UI via `app` modules, which apply `static/styles.css` for a consistent dark theme (e.g., `#181A20` background, `#C70039` accents).
- Data visualizations (e.g., tables in `analysis.py`) reflect the theme with dark backgrounds and hover effects.

## 🚀 Usage
- **Setup**: Ensure `dinemate.db` exists in the `database` folder. Initialize with:
  ```bash
  sqlite3 dinemate.db < database/schema.sql