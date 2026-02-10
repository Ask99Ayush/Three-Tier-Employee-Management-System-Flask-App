# 🧑‍💼 Employee Management System (3-Tier Architecture)

A professional **3-tier web application** built using **Flask, MongoDB, Docker, HTML, and CSS**.  
This project demonstrates clean architecture, environment-based configuration, and full CRUD functionality with a modern dark-themed UI.

---

## 🏗️ Architecture Overview

This application follows a **strict 3-tier architecture**:

1. **Presentation Layer**
   - HTML5 templates
   - Custom CSS (dark theme, animations, responsive)

2. **Application Layer**
   - Flask (routing, validation, control flow)
   - Environment-based configuration using `python-dotenv`

3. **Data Layer**
   - MongoDB
   - PyMongo
   - Isolated database logic
   - Docker-ready setup

---

## ✨ Features

- Create, Read, Update, Delete employees
- Clean separation of concerns
- Secure environment variables using `.env`
- Dockerized application
- MongoDB persistent storage
- Modern UI (no Bootstrap / Tailwind)

---

## 🧾 Employee Fields

- Full Name
- Email
- Department
- Role
- Salary
- Date of Joining
- Status (Active / Inactive)

---

## 📂 Project Structure

```

.
├── app.py
├── database/
│   └── mongo.py
├── templates/
│   ├── index.html
│   ├── add.html
│   └── edit.html
├── static/
│   └── style.css
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── .gitignore

````

---

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://mongo:27017
DATABASE_NAME=employee_management
````

> ⚠️ `.env` is ignored by Git for security reasons.

---

## 🐳 Run with Docker (Recommended)

```bash
docker-compose up --build
```

Access the app:

```
http://localhost:5000
```

---

## 🛠️ Run Locally (Without Docker)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## 🎯 Learning Outcomes

* Real-world 3-tier application design
* Flask + MongoDB integration
* Docker-based deployment
* Secure configuration handling
* Clean, maintainable codebase

---
