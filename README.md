
# 🏥 MedApp – AI-Powered Pharmacy & Doctor Management System

MedApp is an **AI-powered full-stack healthcare management system** designed to simplify and streamline pharmacy and doctor management operations through a centralized platform.

The application provides a unified system for managing **doctors, medicines, inventory, suppliers, users, and orders**, along with an interactive dashboard, analytics, reports, smart search, authentication, and AI-powered functionality.



## 🚀 Project Overview

MedApp combines **Artificial Intelligence, Full-Stack Web Development, and Database Management** to provide a smart and efficient healthcare management platform.

The main objective of this project is to reduce manual management, organize healthcare-related data, improve medicine and inventory management, simplify order tracking, and provide an easy-to-use interface for pharmacies, doctors, and administrators.



## ✨ Key Features

### 🤖 AI-Powered Features
- AI-powered healthcare assistance
- Smart search functionality
- Intelligent data handling
- AI-based features for improving healthcare workflows

### 👨‍⚕️ Doctor Management
- Doctor profile management
- Add, update and manage doctor information
- Organized doctor records
- Doctor-wise appointment information

### 💊 Medicine & Inventory Management
- Add and manage medicines
- Update medicine information
- Monitor medicine stock
- Inventory tracking
- Medicine search functionality

### 📦 Supplier Management
- Add and manage suppliers
- Maintain supplier information
- Manage supplier-related medicine records

### 🛒 Order Management & Tracking
- Create and manage orders
- Track order status
- Order processing workflow
- Order tracking from placement to delivery

### 📋 Order Status

The system supports different order stages:

**Placed → Confirmed → Shipped → Out for Delivery → Delivered**

### 👥 User Management
- User registration
- Secure authentication
- User management
- Role-based access
- User information management

### 📊 Dashboard & Analytics
The dashboard provides important system statistics such as:

- Total Doctors
- Total Medicines
- Registered Users
- Suppliers
- Orders
- Inventory information
- Reports and analytics
- Doctor-wise appointment statistics
- Order status statistics

### 🔍 Smart Search
- Search medicines
- Search doctors
- Search suppliers
- Organized search results
- Faster access to healthcare records

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask
- REST APIs
- Flask-JWT

### Database
- Oracle Database
- SQLAlchemy ORM

### AI
- Python-based AI functionality
- Intelligent search and data processing

### Tools
- Git
- GitHub
- VS Code
- Oracle SQL Developer

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────────┐
                 │       MedApp UI         │
                 │ HTML / CSS / JavaScript │
                 │       Bootstrap         │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │      Flask Backend      │
                 │       REST APIs         │
                 │   Business Logic        │
                 │ Authentication / JWT    │
                 └────────────┬────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
      ┌──────────────────┐       ┌──────────────────┐
      │   AI Features    │       │ SQLAlchemy ORM   │
      │ Smart Functions  │       │ Database Layer   │
      └──────────────────┘       └────────┬─────────┘
                                          │
                                          ▼
                                ┌──────────────────┐
                                │ Oracle Database  │
                                └──────────────────┘

---

## 📂 Project Structure

```text
MedApp/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── routes/
│   ├── auth.py
│   ├── medicine.py
│   ├── order.py
│   ├── supplier.py
│   ├── user.py
│   ├── dashboard.py
│   ├── report.py
│   └── search_result.py
│
├── models/
│   ├── user.py
│   ├── medicine.py
│   ├── order.py
│   ├── supplier.py
│   └── doctor.py
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── scripts/

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/YOUR-REPOSITORY.git
```

### 2. Open the Project Folder

```bash
cd MedApp
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 🗄️ Oracle Database Configuration

MedApp uses **Oracle Database** for storing application data.

Create a `.env` file in the project root directory and add your database configuration:

```env
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
API_PREFIX=/api/v1
```

Replace the values with your own Oracle Database credentials.

> ⚠️ Never upload your `.env` file, passwords, API keys, or other sensitive credentials to GitHub.

---

## ▶️ Run the Application

After configuring the database, run:

```bash
python app.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

Open the URL in your browser to access MedApp.

---

## 🔐 Security

MedApp includes security mechanisms such as:

- JWT-based authentication
- Secure user authentication
- Role-based access
- Protected API endpoints
- Environment variable configuration
- Database authentication

Sensitive credentials are kept outside the source code using environment variables.

---

## 📊 Dashboard

MedApp provides an interactive dashboard for monitoring healthcare and pharmacy operations.

The dashboard can display:

```text
👨‍⚕️ Total Doctors
💊 Total Medicines
👥 Registered Users
📦 Total Suppliers
🛒 Total Orders
📈 Analytics
📋 Reports
```

The system also supports graphical analysis such as:

- Doctor-wise appointments
- Medicine inventory
- Order status distribution
- Monthly order statistics
- Healthcare management analytics

---

## 🎯 Project Objectives

The major objectives of MedApp are:

- Digitize pharmacy management
- Simplify doctor management
- Manage medicine inventory efficiently
- Maintain supplier records
- Manage and track orders
- Provide secure user management
- Centralize healthcare-related information
- Improve search and data accessibility
- Integrate AI-powered functionality
- Reduce manual administrative work

---

## 📚 Learning Outcomes

Working on MedApp helped me gain practical experience in:

- Full-Stack Web Development
- Python Programming
- Flask Framework
- REST API Development
- Oracle Database
- SQLAlchemy ORM
- Database Design
- CRUD Operations
- Authentication & Authorization
- JWT
- Frontend Development
- Backend Development
- AI Integration
- Git & GitHub
- Software Architecture
- Debugging and Problem Solving

---

## 🔮 Future Improvements

Future versions of MedApp may include:

- Advanced AI-powered healthcare assistant
- AI-based medicine recommendation
- Prescription analysis
- OCR-based prescription processing
- Advanced healthcare analytics
- Notification and alert system
- Mobile application
- Cloud deployment
- Advanced role-based access control
- Real-time notifications

---

## 👨‍💻 Developer

### Aditya Prasad

**Python Developer | Full-Stack Developer | AI Enthusiast**

Technologies:
`Python` `Flask` `Oracle` `SQL` `JavaScript` `HTML` `CSS` `Bootstrap` `REST API` `SQLAlchemy` `Git` `GitHub` `AI`


## ⭐ Project

If you find this project useful or interesting, feel free to the repository.


## 📄 License

This project is developed for **educational, learning, and portfolio purposes**.
