# 🥗 Zero-Waste Recipe Generator ♻️

A Django-based web application that helps reduce food waste by allowing users to:
- Generate AI-powered recipes based on available ingredients
- Track expiring food items
- Share surplus food with the community

---

## 🌟 Features

- **AI Recipe Generator** – Uses OpenAI to generate custom recipes based on ingredients you input  
- **Ingredient Expiry Tracker** – Allows users to log food items and get expiry notifications  
- **Community Food Sharing** – Share and claim surplus food items  
- **User Dashboard** – View liked, saved, shared recipes and donation/claim history  
- **Notification System** – Alerts users about ingredient expiry and system messages  

---

## 🛠️ Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Database:** SQLite (via `db.sqlite3`)
- **AI Integration:** OpenAI API
- **Auth:** Django Authentication System

---

## 🚀 Installation & Run Instructions

### Prerequisites

- Python 3.8+ installed
- pip installed

---

### 🔧 1. Unzip the Project
Unzip the folder you downloaded or received (e.g., `Zero-Waste-Recipe-Generator`).

---

### ⚙️ 2. Create & Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📦 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

### 🗄️ 4. Database Setup
You do not need to run migrations — db.sqlite3 is already included with preloaded data.
If needed, you can run:
```bash
python manage.py migrate
```

---

### ▶️ 5. Start the Server
```bash
python manage.py runserver
```
Then open your browser and visit:
http://127.0.0.1:8000/

---

### 💡 Usage Guide
- Register/Login to access features
- Add Ingredients with optional expiry dates
- Generate Recipes using AI based on what you have
- Share or Save Recipes, or track them in your dashboard
- Get Notifications when ingredients are expiring soon
- Share Surplus Food or claim it from others

---

### 🧪 Sample Accounts 
- Email: hello@gmail.com
- Password: hello123

---

### 📂 Project Structure
```javascript
Zero-Waste-Recipe-Generator/
├── ai_recipe/
├── ingredient_tracker/
├── notification/
├── recipe/
├── community/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

```
---
### 📜 License
This project is submitted for academic purposes. The Hugging Face API is used under free-tier credits.

---

### 🙏 Acknowledgments
- Hugging Face AI – for recipe generation
- Django – for web framework
- Team members and instructors – for collaboration and guidance
