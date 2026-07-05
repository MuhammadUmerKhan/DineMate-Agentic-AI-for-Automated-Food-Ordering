# 🍽️ **DineMate: Agentic AI for Automated Food Ordering 🎙️**

## 📌 **Overview**
**DineMate** is an **AI-driven, agent-based food ordering system** designed to streamline **ordering, tracking, and management** for customers, kitchen staff, and restaurant admins. Built with **Large Language Models (LLMs)**, **LangChain**, **LangGraph**, and **Streamlit**, it offers a **fully automated, real-time food ordering experience** with an intelligent chatbot, kitchen dashboard, and admin analytics. Recently enhanced with a centralized dark theme (via `static/styles.css`) and SQLite database integration, DineMate provides a cohesive, food-inspired UI and robust backend support.

---
![](https://www.streebo.com/blog/wp-content/uploads/2020/02/restaurant-chatbot-thumbnail.jpg)

## 🚀 **Key Features**

### ✅ **For Customers:**
- 🛒 **Browse the Menu**: View real-time prices and items in a styled interface.
- 🍔 **Order Food**: Use a natural language chatbot or voice commands to place orders.
- 🔄 **Modify Orders**: Adjust items or quantities before confirmation.
- 🚫 **Cancel Orders**: Cancel within 10 minutes of placement.
- 📦 **Track Orders**: Monitor status (Pending, Delivered, etc.) in real time.
- 💳 **Bill Calculation**: Get instant total price before checkout.
- 🎤 **Voice Ordering**: Place orders hands-free with speech-to-text and text-to-speech.

### ✅ **For Kitchen Staff:**
- 🔥 **View Orders**: Access only confirmed (non-cancelable) orders (10+ minutes old).
- 🔄 **Update Status**: Change order status (e.g., In Process → Completed) via a real-time dashboard.
- 🚀 **Efficiency**: Auto-refreshed UI for seamless kitchen management.

### ✅ **For Customer Support:**
- 📝 **Modify Orders**: Update items, quantities, or prices within the 10-minute window.
- 🚫 **Cancel Orders**: Handle cancellations on behalf of customers if eligible.
- 📦 **Manage Orders**: Oversee all active and completed orders with detailed tracking.

### ✅ **For Admin (Restaurant Owner/Manager):**
- 🛡️ **Update Prices**: Adjust menu prices directly from the dashboard.
- ➕ **Add Items**: Introduce new food items to the menu.
- 🗑️ **Remove Items**: Delete existing items with confirmation.
- 📊 **Analytics Dashboard**: Gain insights into revenue, trends, and customer behavior.

---

## 📊 **Business Analytics Dashboard for Admins!**

### 📌 **What’s Inside?**
A **data-driven dashboard** empowering admins with actionable insights to optimize restaurant operations.

- 🔹 **📆 Revenue Trends**: Interactive monthly and yearly revenue charts.
- 🔹 **🍽️ Most Ordered Items**: Identify top-selling menu items.
- 🔹 **⏳ Peak Ordering Hours**: Optimize staffing based on demand patterns.
- 🔹 **💰 Spending Patterns**: Analyze customer spending habits and high-value trends.
- **📈 Data-Driven Decisions**: Boost profit and streamline operations with real-time analytics.

---

## 🏗️ **Technologies Used**

### 🔹 **Backend & AI**
- 🧠 **openai/gpt-oss-120b**: Powerful LLM for understanding food-related queries.
- 🔗 **LangChain**: Connects LLM with tools and database queries.
- 🔄 **LangGraph**: Manages conversation flow and multi-agent workflows.
- 🐍 **Python**: Core language for chatbot and backend logic.
- 🎤 **Whisper ASR**: Converts spoken orders to text.
- 🗣️ **Torch TTS**: Generates natural speech responses (local use only).
- 🎙️ **Sounddevice & Pydub**: Handles microphone recording and audio processing.

### 🔹 **Database Management**
- 🛢️ **SQLite3**: Stores menu, orders, and user data with optimized indexing.
- 🔑 **Secure Authentication**: Uses hashed passwords for user security.

### 🔹 **Frontend & UI**
- 🌐 **Streamlit**: Interactive UI for chatbot and dashboards.
- 📊 **Plotly & Pandas**: Visualizes data with dark-themed charts.
- 🎨 **Custom CSS**: Centralized `static/styles.css` for a consistent dark theme (#181A20, #C70039 accents).

---

## 🔍 **Project Structure**

```bash
DineMate-Food-Ordering-Chatbot/
│── app/
│   ├── home.py            # 🏠 Home page with feature overview
│   ├── login.py           # 🔐 User login and authentication
│   ├── register.py        # 📝 User registration
│   ├── track_order.py     # 📦 Order tracking for customers
│   ├── order_management.py # 📋 Order management for support staff
│   ├── add_remove_items.py # ➕ Add/remove menu items for admins
│   ├── update_prices.py   # 💰 Price updates for admins
│   ├── kitchen.py         # 👨‍🍳 Kitchen order dashboard
│   ├── analysis.py        # 📊 Analytics dashboard
│   ├── preprocesser.py    # 🛠️ Data preprocessing for analytics
│   ├── visualizers.py     # 📈 Plotly chart generation
│── database/
│   ├── dinemate.db        # 🗄️ SQLite database file
│── scripts/
│   ├── db.py              # 🗄️ Database connection and queries
│   ├── db_handler.py      # 🛒 Order processing logic
│   ├── graph.py           # 📊 Workflow orchestration with LangGraph
│   ├── logger.py          # 📜 Structured logging
│   ├── agent.py           # 🤖 AI agent for chatbot and orders
│   ├── init.py            # 📦 Package initialization
│   ├── state.py           # 🗂️ Session and state management
│   ├── streaming.py       # 🌐 Real-time chatbot streaming
│   ├── tool.py            # 🧰 Utility tools for agents
│   ├── utils.py           # 🧰 Miscellaneous utilities
│── static/
│   ├── styles.css         # 🎨 Centralized dark theme CSS
│── main.py                # 🚀 Main Streamlit app entry point
│── .env.example           # 🔑 Example environment variables
│── requirements.txt       # 📋 Dependency list
│── README.md              # 📖 Project documentation
```

---

## 🛠️ **Agent-Based AI System**
**DineMate leverages a multi-agent system** for dynamic automation:

- 🤖 **Chatbot Agent**: Extracts order details and handles queries.
- 📦 **Order Management Agent**: Manages modifications and cancellations.
- 🔥 **Kitchen Agent**: Updates kitchen staff with non-cancelable orders.
- 🛡️ **Admin Agent**: Facilitates menu and price updates with real-time data.
- **🔄 Seamless Execution**: Agents collaborate using LangGraph for efficient task handling.

---

## 🔑 **User Roles & Functionalities**

| **Role**              | **Accessible Pages**                   | **Allowed Actions**                  |
|-----------------------|---------------------------------------|--------------------------------------|
| **Customer**          | 🏠 Home, 🍔 Chatbot, 📦 Track Order   | Order, Modify, Cancel, Track         |
| **Kitchen Staff**     | 🏠 Home, 👨‍🍳 Kitchen Orders         | View & Update Status                 |
| **Customer Support**  | 🏠 Home, 📦 Order Management          | Modify & Cancel Orders               |
| **Admin**             | 🏠 Home, 🛡️ Update Prices, ➕ Add Items, 📊 Analysis | Update Prices, Manage Menu, Analyze  |

---

## 🚀 **How to Use DineMate?**

### 1️⃣ **Customer Guide**
1. **Login** or **Register** via `login.py`.
2. Use the **🍔 DineMate Chatbot** to order (e.g., "2 burgers and a coke").
3. **Modify** or **Cancel** within 10 minutes.
4. **Track** orders in the 📦 Track Order section.

### 2️⃣ **Kitchen Staff Guide**
1. **Login** as kitchen staff.
2. Access **👨‍🍳 Kitchen Orders** to view and update statuses.

### 3️⃣ **Customer Support Guide**
1. **Login** as support staff.
2. Use **📦 Order Management** to modify or cancel orders.

### 4️⃣ **Admin Guide**
1. **Login** as admin.
2. Manage menu via **🛡️ Update Prices** and **➕ Add/Remove Items**.
3. Explore insights in the **📊 Analysis** dashboard.

---

## 🎙️ **DineMate - AI Voice Ordering Chatbot**

### 🚨 **Why Deployment is Not Possible?**
Voice ordering requires hardware-dependent libraries (e.g., `sounddevice`, `whisper`) unavailable on Streamlit Cloud due to:
- 📌 Version conflicts with `st.chat_message`.
- 🎤 No microphone access in cloud environments.
- 🛠️ Missing dependencies like `FFmpeg` and `Torch TTS`.

**Solution**: Run locally with the setup below.

---

## 🛠️ **Setup Instructions**

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/MuhammadUmerKhan/DineMate-Agentic-AI-for-Automated-Food-Ordering.git
cd DineMate-Food-Ordering-Chatbot
```

### 2️⃣ **Set Up Virtual Environment (Python 3.10)**
- Install Python 3.10: [Download](https://www.python.org/downloads/release/python-3100/).
- Create and activate:
  ```bash
  python3 -m venv .venv
  # Windows: .venv\Scripts\activate
  # macOS/Linux: source .venv/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### 3️⃣ **Configure Database**
- Initialize SQLite: `sqlite3 database/dinemate.db < database/schema.sql`.
- Ensure `database/dinemate.db` is populated with menu and order data.

### 4️⃣ **Run the Application**
```bash
streamlit run main.py
```

---

## 🐳 **Dockerization & Deployment**
- **Build**:
  ```bash
  docker build -t muhammadumerkhan/dinemate-agentic-foodbot .
  ```
- **Run**:
  ```bash
  docker run -p 8501:8501 muhammadumerkhan/dinemate-agentic-foodbot
  ```
- **Push**:
  ```bash
  docker push muhammadumerkhan/dinemate-agentic-foodbot
  ```
- **Pull**:
  ```bash
  docker pull muhammadumerkhan/dinemate-agentic-foodbot
  ```

---

## 🎙️ **Voice Ordering Setup**
1. Run locally: `streamlit run main.py`.
2. Click the **🎤 Microphone Button** in the chatbot.
3. Speak your order (e.g., "I want a pizza").
4. Receive voice feedback confirming the order.

---

## 🏗️ **Recent Enhancements**
- 🎨 **Centralized Styling**: Introduced `static/styles.css` for a dark theme (#181A20 background, #C70039 accents) across all UI elements (tables, inputs, charts).
- 🗄️ **SQLite Transition**: Replaced MySQL with SQLite for simplified deployment and local testing.
- 🤖 **Agent Improvements**: Enhanced `agent.py` and `graph.py` with LangGraph for multi-agent coordination (chatbot, kitchen, admin).
- 📊 **Analytics Upgrade**: Added `preprocesser.py` and `visualizers.py` for advanced data processing and Plotly charts.
- 🧠 **Smart Context Management**: Implemented short-term memory via dynamic conversation summarization (triggered after 10 messages) to optimize token usage while preserving long-term coherence.
- 🛠️ **Script Modularity**: Expanded `scripts` with `state.py`, `tool.py`, and `__init__.py` for better state management and utilities.

---

## 📌 **Where Can This Be Used?**
- 🏪 **Restaurants & Cafés**: AI-powered ordering.
- 🚀 **Online Delivery Apps**: Enhanced customer experience.
- 🏨 **Hotels & Resorts**: Menu interaction.
- 📟 **Self-Ordering Kiosks**: Reduced manual effort.

---

## 📽️ **Live Demo**
- [Click Here](https://dinemate-ai-powered-conversational-ai-agent-for-food-ordering.streamlit.app/?embed_options=dark_theme)

---

## 🔐 **AI Security — Red-Teamed & Hardened**
DineMate's agentic order-management tools were red-teamed against the **OWASP LLM Top 10** and **MITRE ATLAS**, covering prompt injection, excessive agency, system prompt/tool-schema leakage, IDOR, and unbounded consumption. Confirmed findings included a critical price-tampering bug (agent-writable order totals, now fixed with server-side recomputation) and a critical IDOR gap (accepted as a documented residual risk), plus a Prompt Guard 2 input guardrail added ahead of the agent.

📄 **Full report, methodology, findings table, before/after results, and screenshots:** [`SECURITY.md`](./SECURITY.md)

---

## 🤝 **Contributions**
Contributions are welcome! Fork, submit pull requests, or suggest improvements.

---

**© 2025 DineMate AI | Built with ❤️ by Muhammad Umer Khan** 🚀🍔
