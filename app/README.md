# DineMate `app` Folder README 🍽️

This README provides an overview of the Python files in the `app` folder of the **DineMate** project, an AI-powered food ordering system. Each file is a Streamlit module responsible for specific functionality, styled with a consistent dark theme (via `static/styles.css`) to deliver an intuitive, food-inspired user experience. Below is a detailed breakdown of each file's purpose and key features, designed to streamline restaurant operations and enhance customer engagement.

## 📂 Folder Structure
The `app` folder contains the core application logic for DineMate's Streamlit-based UI, interacting with the SQLite database, AI chatbot, and analytics engine. All files leverage the centralized `styles.css` for a cohesive dark theme with food-themed accents (e.g., 🍔, 🍕, #C70039, #FFA500).

## 📄 File Descriptions

- **🛠️ `add_remove_items.py`**
  - **Purpose**: Enables admins to manage menu items by adding or removing them.
  - **Key Features**:
    - ➕ Add new items with name and price, validated against duplicates and invalid inputs.
    - 🗑️ Remove existing items from the menu with confirmation.
    - 📜 Displays the current menu in a styled DataFrame with hover effects.
    - 🔒 Admin-only access with role-based validation.
    - 📊 Uses SQLite database for persistent storage and structured logging for debugging.
  - **Dependencies**: `streamlit`, `pandas`, `scripts.db`, `scripts.logger`.

- **📊 `analysis.py`**
  - **Purpose**: Provides a comprehensive analytics dashboard for business insights.
  - **Key Features**:
    - 💰 Visualizes revenue trends (monthly/yearly) using Plotly charts.
    - 🍽️ Analyzes popular items, order statuses, and peak ordering hours.
    - 🛒 Displays customer spending patterns (histograms, boxplots) and average order value (AOV) trends.
    - 🔍 Offers filters for status (e.g., Delivered, Canceled) and years (2023–2025).
    - 🏆 Provides actionable insights for menu optimization, staffing, and promotions.
    - 🔄 Auto-refreshes every 10 seconds for real-time updates.
  - **Dependencies**: `streamlit`, `pandas`, `scripts.db`, `app.visualizers`, `app.preprocesser`, `scripts.logger`, `streamlit_autorefresh`.

- **🏠 `home.py`**
  - **Purpose**: Renders the DineMate home page, introducing the platform's features.
  - **Key Features**:
    - 📌 Showcases DineMate’s AI-driven capabilities (chatbot, voice ordering, analytics).
    - 🛠️ Details core features, database performance, and user roles via styled expanders.
    - 🚀 Includes a "Getting Started" guide and technology stack overview.
    - 🔗 Links to the GitHub repository for source code access.
    - 🎨 Uses food-themed emojis and markdown for an engaging, agentic UI.
  - **Dependencies**: `streamlit`, `scripts.logger`.

- **👨‍🍳 `kitchen.py`**
  - **Purpose**: Provides an interface for kitchen staff to manage order statuses.
  - **Key Features**:
    - 📦 Displays orders filtered by status (e.g., Pending, Preparing) in a styled DataFrame.
    - 🔄 Allows status updates (e.g., Pending → Delivered) with role-based access for kitchen staff.
    - ⏳ Auto-refreshes every 10 seconds for real-time order tracking.
    - ⚠ Shows access-denied warnings for non-kitchen staff.
    - 📜 Logs all actions for monitoring and debugging.
  - **Dependencies**: `streamlit`, `pandas`, `scripts.db`, `scripts.logger`, `streamlit_autorefresh`.

- **🔐 `login.py`**
  - **Purpose**: Handles user authentication for DineMate.
  - **Key Features**:
    - 👤 Validates username and password against the SQLite database.
    - 🔑 Displays demo credentials in a styled expander for testing.
    - 📝 Redirects to the registration page for new users.
    - 🚪 Supports logout functionality by clearing session state.
    - ⚠ Provides styled error messages for invalid inputs or credentials.
  - **Dependencies**: `streamlit`, `scripts.db`, `scripts.logger`.

- **📦 `order_management.py`**
  - **Purpose**: Enables customer support to manage orders (add, modify, cancel).
  - **Key Features**:
    - ➕ Adds new orders via natural language input (e.g., "2 burgers, 3 cokes").
    - ✏️ Modifies order items or statuses within a 10-minute window.
    - ❌ Cancels orders with time-based validation.
    - 📝 Displays all orders in a styled DataFrame with filtering options.
    - 📜 Logs all operations and handles errors gracefully.
  - **Dependencies**: `streamlit`, `json`, `pandas`, `re`, `scripts.db_handler`, `scripts.db`, `scripts.logger`.

- **🛠️ `preprocesser.py`**
  - **Purpose**: Preprocesses order data for analytics and visualization.
  - **Key Features**:
    - 📅 Extracts temporal features (year, month, hour) from order data.
    - 💰 Calculates monthly and yearly revenue.
    - 🍽️ Aggregates product counts and hourly demand for insights.
    - ⚡ Uses `@st.cache_data` for performance optimization.
    - 📜 Logs preprocessing steps and errors for debugging.
  - **Dependencies**: `streamlit`, `pandas`, `json`, `collections`, `scripts.logger`.

- **📝 `register.py`**
  - **Purpose**: Handles user registration for new DineMate accounts.
  - **Key Features**:
    - 👤 Registers users with username, email, and password.
    - 🔒 Validates against existing usernames/emails to prevent duplicates.
    - 🚀 Redirects to login upon successful registration.
    - ⚠ Displays styled warnings for invalid inputs or registration failures.
    - 📜 Logs registration attempts and outcomes.
  - **Dependencies**: `streamlit`, `scripts.db`, `scripts.logger`.

- **🚚 `track_order.py`**
  - **Purpose**: Allows customers to track order status by ID.
  - **Key Features**:
    - 🔍 Queries order details (items, status, time, date) by order ID.
    - 📦 Displays order information in a styled DataFrame.
    - ⚠ Shows error messages for invalid or non-existent order IDs.
    - 📜 Logs tracking requests and errors.
  - **Dependencies**: `streamlit`, `pandas`, `scripts.db`, `scripts.logger`.

- **🛡️ `update_prices.py`**
  - **Purpose**: Enables admins to update menu item prices.
  - **Key Features**:
    - 💰 Updates prices for existing menu items with validation.
    - 📜 Displays the current menu in a styled DataFrame.
    - 🔒 Restricts access to admins only.
    - ⚠ Provides warnings for invalid items or prices.
    - 📜 Logs price update operations and errors.
  - **Dependencies**: `streamlit`, `pandas`, `scripts.db`, `scripts.logger`.

- **📈 `visualizers.py`**
  - **Purpose**: Generates Plotly charts for the analytics dashboard.
  - **Key Features**:
    - 📊 Creates visualizations for revenue trends, order statuses, popular items, and more.
    - 🕒 Visualizes hourly demand and customer spending patterns.
    - 🎨 Applies dark-themed Plotly styling to match the app’s aesthetic.
    - ⚡ Optimized for performance with reusable chart functions.
    - 📜 Logs chart generation for debugging.
  - **Dependencies**: `plotly.express`, `plotly.graph_objects`, `pandas`, `scripts.logger`.

## 🎨 Theme Integration
- All files import `static/styles.css` to apply a consistent dark theme with food-inspired colors:
  - Background: `#181A20` with a subtle food-themed overlay.
  - Accents: `#C70039` (red, e.g., borders), `#FFA500` (orange, e.g., highlights).
  - Text/Inputs: `#E8ECEF` (light gray) on `#3A4042` (dark gray) backgrounds.
- UI elements (tables, inputs, expanders) feature hover effects, rounded corners, and animations (`fadeIn`, `pulse`) for an agentic, engaging experience.
- Buttons retain their gradient (`#C70039` to `#FFA500`) and pulse animation, as specified.

## 🚀 Usage
- **Run Locally**:
  1. Install dependencies: `pip install -r requirements.txt`.
  2. Ensure `static/styles.css` is in the project root.
  3. Run: `streamlit run main.py`.
- **Access**: Use demo credentials from `login.py` or register a new account.
- **Roles**: Different roles (Admin, Kitchen Staff, Customer Support, Customer) access specific modules based on permissions.

## 🛠️ Dependencies
- Core: `streamlit`, `pandas`, `plotly`, `json`, `re`.
- Custom: `scripts.db`, `scripts.db_handler`, `scripts.logger`, `streamlit_autorefresh`.
- Styling: `static/styles.css` for unified theme.

## 📝 Notes
- Ensure the SQLite database (`database/dinemate.db`) is initialized with menu and order data.
- Voice chat functionality (`main.py`) is disabled on Streamlit Cloud due to library limitations; run locally for full features.
- Logs are stored in `logs/` for debugging and monitoring.
- Source code: [GitHub Repository](https://github.com/MuhammadUmerKhan/DineMate-Agentic-AI-for-Automated-Food-Ordering).

## © 2025 DineMate AI
Built with ❤️ by Muhammad Umer Khan. Powered by AI for a smarter dining experience! 🍔