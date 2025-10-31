# Campus-Management-Portal
# 🏫 Campus Resource Management System

A unified web-based platform designed to streamline campus operations by integrating **Lost & Found**, **Equipment Tracking**, and **Complaint Management** modules.  
This project was built as part of our **DBMS Final Project** using **FastAPI**, **MySQL**, and a simple **HTML/CSS/JS frontend**.

---

## 🚀 Overview

The Campus Resource Management System helps students and administrators manage essential campus activities:

- 📦 **Lost & Found System** – Report lost items or register found ones. Admins can verify and return items.  
- ⚙️ **Equipment Tracker** – Track equipment usage, borrowing, and returns within the campus.  
- 🧾 **Complaint Management** – Students and staff can file complaints which are then handled by administrators.

All three modules share a **common login system** and a **centralized MySQL database**.

---

## 👥 Team Members & Roles

| Member | Module | Responsibilities |
|--------|---------|------------------|
| **Raj Kale** | 🟢 Lost & Found System | Backend (FastAPI), Database Design, API Integration |
| **Abhimanyu Kadhane** | ⚙️ Equipment Tracker | Backend (FastAPI), Equipment APIs, Frontend |
| **Vandan Jethwa** | 🧾 Complaint Management | Backend (FastAPI), Complaint APIs, Frontend |

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Database** | MySQL with SQLAlchemy ORM |
| **Frontend** | HTML, CSS, JavaScript |
| **Authentication** | JWT-based login system |
| **Server** | Uvicorn |

---

## 🗄️ Database Design (Overview)

The system uses a shared `users` table and separate tables for each module.

### 🔹 Lost & Found
- `users(user_id, name, email, password, role)`
- `lost_items(item_id, user_id, item_name, description, date_lost, location_lost, status)`
- `found_items(found_id, user_id, item_name, description, date_found, location_found, matched_item_id)`

### 🔹 Equipment Tracker
- `equipments(equip_id, name, type, location, condition, availability)`
- `borrow_records(record_id, equip_id, user_id, borrow_date, return_date, status)`

### 🔹 Complaint Management
- `complaints(complaint_id, user_id, title, description, category, date_filed, status)`
- `admin_actions(action_id, complaint_id, admin_id, notes, date_action)`

---


## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/campus-mgmt.git
cd campus-mgmt

pip install -r requirements.txt

DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/campus_mgmt"

uvicorn backend.main:app --reload

http://127.0.0.1:8000
```


