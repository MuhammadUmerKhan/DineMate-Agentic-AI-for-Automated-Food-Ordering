# DineMate `scripts` Folder README 🛠️

This README provides an overview of the `scripts` folder in the **DineMate** project, an AI-powered food ordering system. The folder contains Python utility modules that handle core functionalities such as database operations, logging, chatbot processing, state management, agent orchestration, and data streaming. These scripts support the `app` modules and are integrated with the dark-themed UI (via `static/styles.css`) for a seamless, food-inspired experience.

## 📂 Folder Structure
The `scripts` folder includes reusable Python files providing backend logic, database interactions, and agent-driven workflows, ensuring modularity and scalability for DineMate’s operations. The `__init__.py` file enables package import functionality.

## 📄 File Descriptions

- **🗄️ `db.py`**
  - **Purpose**: Manages SQLite database connections and operations.
  - **Key Features**:
    - 🔗 Establishes connections to `database/dinemate.db`.
    - 📝 Handles CRUD operations for menu, orders, and users.
    - ⚡ Implements batch inserts and optimized queries with indexes.
    - 🔒 Validates user credentials and logs all actions.
    - 📜 Integrates with `logger.py` for structured logging.
  - **Dependencies**: `sqlite3`, `scripts.logger`.

- **🛠️ `db_handler.py`**
  - **Purpose**: Provides business logic for order handling.
  - **Key Features**:
    - 📦 Processes order modifications, cancellations, and additions.
    - 🔍 Extracts items and quantities from user input (e.g., "2 burgers, 3 cokes").
    - 💰 Calculates total prices based on the menu.
    - ⏳ Enforces a 10-minute modification/cancellation window.
    - 📜 Logs order-related operations for auditing.
  - **Dependencies**: `scripts.db`, `scripts.logger`.

- **📊 `graph.py`**
  - **Purpose**: Manages workflow orchestration and graph-based processing.
  - **Key Features**:
    - 📈 Defines graph structures for AI-driven order workflows (e.g., LangGraph).
    - 🔄 Coordinates multi-step processes like order validation and pricing.
    - 🤖 Integrates with the AI agent for dynamic decision-making.
    - ⚡ Optimizes execution with asynchronous updates.
    - 📜 Logs graph operations and errors for debugging.
  - **Dependencies**: `langgraph`, `scripts.logger`.

- **📜 `logger.py`**
  - **Purpose**: Implements structured logging for the application.
  - **Key Features**:
    - 🗂️ Configures logging to `logs/` with JSON formatting.
    - 📅 Records timestamps, user actions, and error details.
    - ⚠ Captures warnings and errors for debugging.
    - 🔧 Customizable log levels (info, warning, error).
    - 📊 Used across all modules for consistent monitoring.
  - **Dependencies**: `logging`, `json`.

- **🤖 `agent.py`**
  - **Purpose**: Orchestrates the AI agent for natural language processing and ordering.
  - **Key Features**:
    - 🧠 Utilizes Qwen-2.5-32B LLM for chatbot interactions.
    - 🍔 Interprets user queries (e.g., "Order 2 pizzas") into actionable commands.
    - 🎤 Supports voice input processing via Whisper AI integration.
    - 🔄 Manages agent state and responses in real time.
    - 📜 Logs agent activities and errors.
  - **Dependencies**: `langchain`, `whisper`, `scripts.logger`.

- **📋 `init.py`**
  - **Purpose**: Initializes the `scripts` package for import.
  - **Key Features**:
    - 📦 Enables modular imports (e.g., `from scripts import db`).
    - 🔧 Sets up package-level configurations or utilities.
    - ⚙️ Ensures proper loading of dependent modules.
    - 📜 Logs initialization events if errors occur.
  - **Dependencies**: None (standard Python package file).

- **🗂️ `state.py`**
  - **Purpose**: Manages application and session state.
  - **Key Features**:
    - 💾 Stores user authentication, role, and chat history.
    - 🔄 Updates state dynamically during order processing.
    - 🔒 Secures sensitive data (e.g., username, password hashes).
    - ⚡ Provides fast access for UI rendering in `app.main`.
    - 📜 Logs state changes for debugging.
  - **Dependencies**: `streamlit`, `scripts.logger`.

- **🌐 `streaming.py`**
  - **Purpose**: Handles real-time streaming of chatbot responses.
  - **Key Features**:
    - 🌐 Streams updates from the AI chatbot (e.g., Qwen-2.5-32B).
    - ⏳ Implements asynchronous updates with a StreamHandler.
    - 🍔 Processes natural language orders in real time.
    - 📜 Logs streaming events and errors.
    - 🔄 Integrates with `app.main` for chatbot UI.
  - **Dependencies**: `asyncio`, `scripts.logger`.

- **🧰 `tool.py`**
  - **Purpose**: Provides utility tools for agent and workflow tasks.
  - **Key Features**:
    - 🔧 Offers helper functions for data validation and transformation.
    - 📊 Supports graph and agent toolsets (e.g., menu lookup, price updates).
    - ⚙️ Enhances modularity for reusable logic.
    - 📜 Logs tool usage and errors.
    - 🔄 Integrates with `agent.py` and `graph.py`.
  - **Dependencies**: `scripts.logger`.

- **🧰 `utils.py`**
  - **Purpose**: Contains miscellaneous utility functions.
  - **Key Features**:
    - 💬 Enables chat history for the DineMate chatbot.
    - 🔧 Provides helper functions for session management.
    - 📝 Prints QA pairs for debugging and logging.
    - ⚙️ Supports role-based page access in `app.main`.
    - 📜 Logs utility operations for traceability.
  - **Dependencies**: `streamlit`, `scripts.logger`.

## 🎨 Theme Integration
- The `scripts` modules indirectly support the UI’s dark theme by providing data and logic that render in `app` modules, styled with `static/styles.css` (e.g., `#181A20` background, `#C70039` borders).
- Data from `db.py` and `db_handler.py` powers themed tables and charts in `analysis.py`.

## 🚀 Usage
- **Setup**: Install dependencies via `pip install -r requirements.txt`.
- **Access**: Imported by `app` modules (e.g., `from scripts.db import Database`).
- **Logging**: Configure log paths in `logger.py` if needed.
- **Initialization**: Ensure `__init__.py` is present for package functionality.

## 🛠️ Dependencies
- Core: `sqlite3`, `logging`, `json`, `asyncio`, `streamlit`.
- AI/ML: `langchain`, `langgraph`, `whisper`.
- Custom: Integrated with `app` modules and `static/styles.css` for UI consistency.

## 📝 Notes
- Ensure `database/dinemate.db` is accessible for `db.py` operations.
- Logs are stored in `logs/` for debugging; rotate logs as needed.
- Voice chat functionality requires local setup (see `main.py` for details).
- Source code: [GitHub Repository](https://github.com/MuhammadUmerKhan/DineMate-Agentic-AI-for-Automated-Food-Ordering).

## © 2025 DineMate AI
Built with ❤️ by Muhammad Umer Khan. Powering a smarter dining experience! 🍕