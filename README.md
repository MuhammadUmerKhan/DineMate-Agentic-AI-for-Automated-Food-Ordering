# 🍽️ **DineMate: AI-Powered Conversational Agent for Smart Food Ordering**  

## 📌 **Overview**  
**DineMate** is an **AI-driven, agent-based food ordering system** that streamlines the **ordering, tracking, and management** process for customers, kitchen staff, and restaurant admins. It integrates an **intelligent chatbot**, a **kitchen dashboard**, and an **admin panel** for seamless restaurant operations.  

---
![](https://www.streebo.com/blog/wp-content/uploads/2020/02/restaurant-chatbot-thumbnail.jpg)

It is built using **Large Language Models (LLMs)**, **LangChain**, **LangGraph**, **MySQL**, and **Streamlit** for a **fully automated, real-time food ordering experience**.

---

## 🚀 **Key Features**  

### ✅ **For Customers:**  
- 🛒 **Browse the menu** and check real-time prices.  
- 🍔 **Order food items** using a natural language chatbot.  
- 🔄 **Modify existing orders** before confirmation.  
- 🚫 **Cancel an order** within **10 minutes** of placement.  
- 📦 **Track your order status** in real time.  
- 💳 **Get the total bill calculation** instantly before checkout.  
- 🎤 **Voice-Based Ordering** – Place orders using voice commands.  

### ✅ **For Kitchen Staff:**  
- 🔥 **View only confirmed (non-cancelable) orders** (orders placed **10+ minutes ago**).  
- 🔄 **Update order status** (*e.g., In Process → Ready → Completed*).  
- 🚀 **Real-time dashboard for kitchen orders**.  

### ✅ **For Customer Support:**  
- 📝 **Modify orders** (update items, quantities, or total price).  
- 🚫 **Cancel orders** on behalf of customers (if within the allowed time).  
- 📦 **Manage and track all active and completed orders**.  

### ✅ **For Admin (Restaurant Owner/Manager):**  
- 🛡️ **Update menu prices** directly from the dashboard.  
- ➕ **Add new food items** to the restaurant menu.  
- 🗑️ **Remove existing items** from the menu.  
- 📊 **View business insights with a powerful analytics dashboard.**  

---

## 📊 **Business Analytics Dashboard for Admins!**  

### **📌 What’s Inside?**  
A **powerful data-driven dashboard** that provides insights into restaurant operations, helping **owners & managers make informed decisions**.  

🔹 **📆 Revenue Trends:** View **monthly & yearly earnings** with **interactive graphs**.  
🔹 **🍽️ Most Ordered Items:** Find out which **menu items are top sellers**.  
🔹 **⏳ Peak Ordering Hours:** Optimize staffing by knowing **when orders peak**.  
🔹 **💰 Customer Spending Patterns:** Identify high-value customers & spending trends.  

**📈 Data-Driven Insights = More Profit & Better Operations! 🚀**  

---

## 🏗️ **Technologies Used**  

### 🔹 **Backend & AI**  
- 🧠 **Qwen** – A **powerful LLM** that understands **food-related queries**.  
- 🔗 **LangChain** – Connects LLM with **external tools like MySQL**.  
- 🔄 **LangGraph** – Handles **conversation flow, decision-making, and tool execution**.  
- 🐍 **Python** – Main programming language for the chatbot logic.  
- 🎤 **Whisper ASR** – Converts **spoken orders into text** (Speech-to-Text).  
- 🗣️ **Torch TTS** – Converts **text responses into natural speech** (Text-to-Speech).  
- 🎙️ **Sounddevice & Pydub** – Enables **microphone recording & audio processing**.  

### 🔹 **Database Management**  
- 🛢️ **MySQL/SQLite3** – Stores **menu items, orders, users, and status updates**.  
- 🔑 **Secure authentication** with **hashed passwords**.  

### 🔹 **Frontend & UI**  
- 🌐 **Streamlit** – **Interactive UI** for chatbot and order management.  
- 📊 **Plotly & Pandas** – **Data visualization & business insights**.  
- 🎨 **Custom CSS & HTML** – Enhances **chatbot appearance and styling**.  

---

## 🔍 **Project Structure**  

```bash
DineMate-Food-Ordering-Chatbot/
│── app/
│   ├── home.py               # 🏠 Home page
│   ├── login.py              # 🔐 User login & authentication
│   ├── track_order.py        # 📦 Customer Order Tracking
│   ├── order_management.py   # 📋 Customer Support Order Management
│   ├── add_remove_items.py   # ➕ Admin: Add/Remove Items
│   ├── update_prices.py      # 💰 Admin: Update Item Prices
│   ├── kitchen.py            # 👨‍🍳 Kitchen Staff Order Dashboard
│   ├── register.py           # 📝 User Registration Page - Allows new customers to sign up.
│   ├── voice_chat.py              # 🎤 Voice-Based Ordering (STT & TTS)
│── bot/
│   ├── agent.py              # 🤖 AI Chatbot logic using LangGraph
│── database/
│   ├── db.py                 # 🗄️ Database connection & query functions
│── foodbot_schema.sql
│── order/
│   ├── order_handler.py       # 🛒 Order Processing Logic
│── main.py                    # 🚀 Main Streamlit App
│── config.py                 # 🔧 Database Configuration
│── README.md                  # 📖 Project Documentation
```
---
## 🛠️ **Agent-Based AI System**  

**DineMate leverages AI agents** to automate various tasks dynamically:  

🤖 **Chatbot Agent:** Extracts order details, answers queries, and handles menu browsing.  
📦 **Order Management Agent:** Manages **order modifications & cancellations**.  
🔥 **Kitchen Agent:** Automatically updates kitchen staff with **non-cancelable orders**.  
🛡️ **Admin Agent:** Allows **menu & price modifications** based on **real-time database queries**.  

#### This **multi-agent system ensures smooth task execution** without requiring manual intervention.
---

## 🔑 **User Roles & Functionalities**  

| **Role**              | **Accessible Pages**                   | **Allowed Actions** |
|----------------------|--------------------------------------|---------------------|
| **Customer**        | 🏠 Home, 🍔 Chatbot, 📦 Track Order   | Order, Modify, Cancel, Track Orders |
| **Kitchen Staff**   | 🏠 Home, 👨‍🍳 Kitchen Orders         | View & Update Order Status |
| **Customer Support** | 🏠 Home, 📦 Order Management       | Modify & Cancel Orders |
| **Admin**           | 🏠 Home, 🛡️ Update Prices, ➕ Add Items, 📊 Business Dashboard | Update Prices, View Analytics |

---

## 🚀 **How to Use DineMate?**  

### **1️⃣ Customer Guide**
1. **Login** or **Register** as a new customer.  
2. Go to **"🍔 DineMate Chatbot"** and start chatting!  
3. Order food in **natural language**, e.g.:
   - *"I want 1 Margherita Pizza and 2 Cokes."*  
   - *"Replace Coke with Mango Juice."*  
4. Confirm your order and **get the total price**.  
5. **Track your order** in **📦 Track Order** section.  

### **2️⃣ Kitchen Staff Guide**
1. **Login as Kitchen Staff**.  
2. Access **"👨‍🍳 Kitchen Orders"** section.  
3. View **all confirmed orders (older than 10 minutes)**.  
4. **Update order status** (*e.g., Preparing → Ready*).  

### **3️⃣ Customer Support Guide**
1. **Login as Customer Support**.  
2. Go to **"📦 Order Management"** section.  
3. **Modify orders**, **cancel orders**, or **update statuses**.  

### **4️⃣ Admin Guide**
1. **Login as Admin**.  
2. Manage restaurant **menu & pricing**:
   - **"🛡️ Update Prices"** – Modify existing prices.  
   - **"➕ Add/Remove Items"** – Add or remove menu items.  

---

## 🎙️ **DineMate - AI Voice Ordering Chatbot**  

## 🚨 **Why Deployment is Not Possible?**  

DineMate's **voice-based ordering** feature requires several **hardware-dependent** and **version-specific** libraries that **cannot run** on **Streamlit Cloud**:  

### 🔥 **Key Issues**:  
1. **Streamlit Version Conflict** - `st.chat_message` is unavailable in older Streamlit versions.  
2. **Microphone Access (`sounddevice`)** - Cloud environments do not support direct microphone input.  
3. **Speech-to-Text (`whisper`)** - Requires `FFmpeg`, which is **not pre-installed** on Streamlit Cloud.  
4. **Text-to-Speech (`Torch TTS`)** - Needs **GPU acceleration**, unavailable on Streamlit Cloud.  
5. **Dependency Issues** - Libraries like `pydub`, `numpy`, and `wave` have **strict version requirements**.  

Thus, **DineMate Voice Ordering must be run locally**! 🚀  

---

## 🛠️ **1. Setting Up a Virtual Environment (Python 3.10)**  

### 🔹 **Step 1: Install Python 3.10 (if not installed)**  
Check if Python 3.10 is installed:  
```bash
python3 --version
```
If not installed, download from: [Python 3.10 Download](https://www.python.org/downloads/release/python-3100/)  

### 🔹 **Step 2: Create a Virtual Environment**  
Run the following commands:  
```bash
# Create virtual environment
python3 -m venv dinemate_env  

# Activate the virtual environment  
# Windows  
dinemate_env\Scripts\activate  

# macOS/Linux  
source dinemate_env/bin/activate  
```

### 🔹 **Step 3: Install Dependencies**  
Ensure you have **pip** updated, then install the required packages:  
```bash
pip install --upgrade pip  

# Install required libraries  
pip install -r requirements.txt  
```
If `requirements.txt` is missing, install manually:  
```bash
pip install streamlit==1.22.0  
pip install sounddevice numpy wave whisper pydub torch TTS  
pip install openai langchain ffmpeg-python  
```

---

## 🚀 **2. How to Run the DineMate Voice Ordering Chatbot Locally?**  
After setting up the virtual environment:  

1. Navigate to the project folder:  
   ```bash
   cd dinemate-ai
   ```
2. Run the Streamlit app:  
   ```bash
   streamlit run app.py
   ```
3. Open the **local browser link** provided by Streamlit.  

---

## 🎙️ **3. How to Use Voice-Based Ordering?**  

1. Click on the **Microphone Button** in the chatbot interface.  
2. Speak your order naturally, e.g., *"I want a cheeseburger and a Coke."*  
3. The chatbot converts your **speech to text** and processes the order.  
4. The bot responds with **voice feedback** confirming your order.  

This feature enhances **accessibility and user experience** for hands-free ordering!  

💡 **Now you can run DineMate Voice Ordering on your local machine!** 🚀🎙️

---

## 🏗️ **How It Works?**  

### **1️⃣ Order Processing**
- AI **agents** extract **items & quantities** from user messages.  
- The chatbot **queries the database** for menu availability.  
- Calculates **total price dynamically** before confirmation.  

### **2️⃣ Order Confirmation & Status Updates**
- Saves the order in **SQLite3/MySQL** after confirmation.  
- The **Kitchen Agent auto-updates the kitchen dashboard**.  

### **3️⃣ Order Cancellation Rules**
- Customers can cancel **within 10 minutes**.  
- After 10 minutes, **only Customer Support can cancel orders**.  

---

## 🛠️ **Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot.git
cd DineMate-Food-Ordering-Chatbot
```

### **2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Configure Database**  
- Create a **MySQL Database** and import the provided SQL file.  
- Update `config.py` with **database credentials**.  

### **4️⃣ Run the Application**  
```bash
streamlit run main.py
```

---

## 📌 **Where Can This Be Used?**  
- **Restaurants & Cafés** 🏪 – AI-powered food ordering.  
- **Online Food Delivery Apps** 🚀 – Seamless customer experience.  
- **Hotels & Resorts** 🏨 – AI-driven menu interaction.  
- **Self-Ordering Kiosks** 📟 – Reduce manual workload.  

---
## 📽️ Live Demo:
- [Click Here](https://dinemate-ai-powered-conversational-ai-agent-for-food-ordering.streamlit.app/?embed_options=dark_theme)
---

## 🤝 **Contributions**  
Contributions are **welcome**! Feel free to **fork this project**, submit **pull requests**, or **suggest improvements**.  

**View Source Code:** [GitHub Repository](https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot)  

---

**© 2025 DineMate AI | Built with ❤️ by Muhammad Umer Khan** 🚀🍔
