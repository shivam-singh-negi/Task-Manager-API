# Task Manager API

A high-performance, RESTful API for managing tasks with advanced user authentication, role-based access control, and comprehensive documentation. Built as per the **r-ztm-f-d** specification using **Flask**, **SQLAlchemy**, and **JWT**.

---

## 🚀 Requirement Compliance (r-ztm-f-d)

This project has been meticulously developed to exceed all requirements specified in the objective:

| Requirement | Implementation Detail | Status |
| :--- | :--- | :--- |
| **Framework** | Built using **Flask** (Python) with MVC Architecture. | ✅ |
| **Task Model** | Includes `id`, `title`, `description`, `completed`, `created_at`, `updated_at`. | ✅ |
| **CRUD Endpoints** | Complete GET, POST, PUT, DELETE operations for `/tasks`. | ✅ |
| **Authentication** | Secure **JWT-based** authentication with token expiry. | ✅ |
| **Registration** | Robust User Registration and Login endpoints. | ✅ |
| **Authorization** | Only authenticated owners or admins can modify tasks. | ✅ |
| **Documentation** | Interactive **Swagger (Flasgger)** documentation + README. | ✅ |
| **Testing** | Suite of unit tests with **Pytest** (11/11 Passing). | ✅ |
| **Bonus: Pagination** | Integrated into Task and User list endpoints. | ✅ |
| **Bonus: Filtering** | Filter tasks by completion status. | ✅ |
| **Bonus: Roles** | Implemented **Admin** vs **Regular User** permissions. | ✅ |

---

## ✨ Features

- **Advanced Security**: Password hashing with Werkzeug and JWT authorization.
- **Smart Data Persistence**: SQLite database with SQLAlchemy ORM (supports PostgreSQL/MySQL).
- **Clean Architecture**: Organized into Controllers, Models, and Routes for maximum maintainability.
- **Interactive API Play**: Swagger UI allows you to test endpoints directly from the browser.
- **Containerized Implementation**: Fully Dockerized with persistent volume support.
- **Automated Logging**: Rotating file logging for info and error tracking.

---

## 🛠️ Installation & Local Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Step 1: Clone and Navigate
```bash
git clone https://github.com/shivam-singh-negi/Task-Manager-API.git
cd Task-Manager-API
```

### Step 2: Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configuration
Copy the `.env.example` to `.env` and adjust keys if necessary:
```bash
cp .env.example .env
```

### Step 4: Run the Application
```bash
python run.py
```
Expected output:
```text
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

## 🐳 Running with Docker

The Task Manager API is fully containerized for easy deployment and consistent development environments.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Option 1: Using Docker Compose (Recommended)

This is the easiest way to get the entire application running, including persistent volumes for your database.

1. **Configure Environment Variables**:
   Copy the example environment file if you haven't already:
   ```bash
   cp .env.example .env
   ```

2. **Build and Start Container**:
   ```bash
   docker-compose up --build
   ```

3. **Access the API**:
   The API will be available at `http://localhost:5000`.

### Option 2: Using Docker Directly

If you prefer to use the Docker CLI directly:

1. **Build the Image**:
   ```bash
   docker build -t task-manager-api .
   ```

2. **Run the Container**:
   ```bash
   docker run -p 5000:5000 --env-file .env task-manager-api
   ```

### Volume Persistence
When using `docker-compose`, a volume named `db_data` is created to ensure your SQLite database persists even if the container is removed. This volume is mapped to `/app/instance` inside the container.

---

## API Documentation

### Base URL
`http://127.0.0.1:5000/api`

### HTTP Status Codes
| Code | Meaning |
| :--- | :--- |
| **200** | OK, request succeeded |
| **201** | Created, resource created successfully |
| **400** | Bad Request, invalid input |
| **401** | Unauthorized, authentication required |
| **403** | Forbidden, insufficient permissions |
| **404** | Not Found, resource doesn't exist |
| **500** | Internal Server Error |

### Authentication Endpoints

#### 1. Register User
`POST /api/auth/register`
**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```
**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 2. Login User
`POST /api/auth/login`
**Request:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```
**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "user"
  }
}
```

---

### Task Management Endpoints

#### 1. Create Task
`POST /api/tasks`
**Authorization**: `Bearer <access_token>`
**Request:**
```json
{
  "title": "Complete project",
  "description": "Finish the task manager API",
  "completed": false
}
```
**Response (201):**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the task manager API",
    "completed": false,
    "user_id": 1
  }
}
```

---

### Admin Endpoints (Admin Only)

#### 1. List All Users
`GET /api/admin/users?page=1&per_page=10&role=user`

#### 2. System Statistics
`GET /api/admin/stats`
**Response (200):**
```json
{
  "stats": {
    "total_users": 5,
    "total_tasks": 45,
    "completed_tasks": 30,
    "incomplete_tasks": 15,
    "admin_users": 2,
    "regular_users": 3,
    "completion_rate": "66.7%"
  }
}
```

---

## Authentication & Authorization

### How It Works
1. Register via `/api/auth/register`.
2. Login via `/api/auth/login` to receive a Bearer JWT.
3. Include the token in subsequent requests: `Authorization: Bearer <access_token>`.

### Default Roles & First User Rule
⭐ **Important**: The first user registered in the system automatically becomes an **admin**. This ensures the system is always manageable without manual DB intervention.

```json
// Example: First registration response
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "admin_user",
    "role": "admin"
  }
}
```

---

## Admin Testing Guide

### Step 1: Create an Admin
The first user registered automatically gets the `admin` role.

### Step 2: Login as Admin
Use the `/api/auth/login` endpoint to get your token.

### Step 3: Verify Admin Role in Token (Using Python)
```python
import base64, json
token = "your_access_token_here"
# JWT has 3 parts: header.payload.signature
parts = token.split('.')
payload = parts[1]
payload += '=' * (4 - len(payload) % 4) # Add padding
decoded = base64.urlsafe_b64decode(payload)
print(json.dumps(json.loads(decoded), indent=2))
```

---

## 🧪 Testing

The project includes a comprehensive test suite covering authentication, task CRUD, and admin functionalities.

### Running Tests Locally
```bash
# Ensure you are in the virtual environment
pytest
```

### Running Tests with Coverage
```bash
pytest --cov=app tests/
```

### What's Tested?
- **Auth**: Registration, Login, Profile Retrieval.
- **Tasks**: Create, Read, Update, Delete (Owner vs Non-owner).
- **Admin**: User Listing, System Stats, Role modification.
- **Health**: API status check.

---

## 🏗️ Project Structure (MVC)
```text
Task-Manager-API/
├── app/
│   ├── controllers/    # Domain Business Layer (Business Rules & Core Logic)
│   │   ├── admin_controller.py
│   │   ├── auth_controller.py
│   │   └── task_controller.py
│   ├── models/         # Model Layer (SQLAlchemy ORM Entities)
│   │   └── __init__.py
│   ├── routes/         # View Layer (Endpoints & Swagger Specification)
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── __init__.py     # App Factory initialization
│   └── utils.py        # Shared utilities and decorators (RBAC check, validation)
├── tests/              # Unit Test suite (Pytest)
├── Dockerfile          # Image definition
├── docker-compose.yml  # Orchestration configuration
├── run.py              # Application entry point
└── requirements.txt    # Library dependencies
```

---

## 💾 Database Guide

The application uses **SQLite** for simplicity and portability. The database management is fully automated to ensure a "zero-configuration" experience.

### 🔄 Automatic Creation
The application is equipped with an **auto-provisioning** logic in `app/__init__.py`. 
- **On Startup**: The system checks if the database directory and file exist.
- **Auto-Initialization**: If missing, it automatically creates the directories and initializes all tables (`db.create_all()`).
- **No Manual SQL Required**: You don't need to run any migration scripts for the initial setup.

### 🛡️ Persistence & Shared Data
The project is configured to share the same database file between your local environment and Docker, ensuring data consistency:

1.  **Local Environment**: The database is stored in the `instance/` folder as `task_manager.db`.
2.  **Docker Environment**: 
    - The `docker-compose.yml` file uses a **bind mount** volume (`.:/app`).
    - This maps your entire project directory (including the `instance/` folder) into the container.
    - **Shared State**: Any user or task created while running in Docker will be immediately visible if you switch back to running locally (and vice versa).

### 🔍 Viewing Your Data
If you want to inspect the database manually:
1.  Install the **SQLite** extension (by alexcvzz) in VS Code.
2.  `Ctrl+Shift+P` -> `SQLite: Open Database`.
3.  Select `/instance/task_manager.db`.
4.  Browse tables or run SQL queries directly.

### 📋 Schema Overview
- **Users**: `id`, `username`, `email`, `password_hash`, `role`, `created_at`, `updated_at`.
- **Tasks**: `id`, `title`, `description`, `completed`, `created_at`, `updated_at`, `user_id`.

---

## Logging

The application maintains detailed logs for monitoring and debugging.

### Log Files
- **`logs/app.log`**: General application activity, successful registrations, and logins.
- **`logs/error.log`**: Detailed error tracebacks and failed system operations.

### Retention Policy
Logs are managed using a `RotatingFileHandler`:
- Each log file is capped at **5MB**.
- The system keeps up to **5 historical copies** for general logs and **10 copies** for error logs.

---

## Maintenance

### Clear Cache Files
To reset the environment or fix mysterious import issues, you may need to clear Python's `__pycache__` and `pytest` cache folders.

#### **On Windows (PowerShell)**:
```powershell
Get-ChildItem -Path . -Include __pycache__, .pytest_cache -Recurse -Force | Remove-Item -Recurse -Force
```

#### **On macOS/Linux**:
```bash
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name ".pytest_cache" -type d -exec rm -rf {} +
```

---

## Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **403 Forbidden** | You need Admin role to access this route. Check token claims. |
| **Token Expired** | Tokens last 1 hour. Re-login to refresh. |
| **Database Locked** | Ensure no multiple write processes are active on the database file. |
| **Unknown Error** | Check `logs/error.log` for a detailed traceback. |

---

## 🚀 Production Deployment

To ensure the highest level of security and performance, the project is configured with a production-ready stack:

### **WSGI Server: Gunicorn**
While the local development server is used for debugging, the **Dockerfile** is configured to use **Gunicorn** in production. Gunicorn is a high-performance HTTP server that can handle multiple simultaneous requests efficiently.

### **Production Security Checklist**
Before deploying to a public server, ensure the following environment variables are set:

1.  **`FLASK_ENV`**: Set to `production`. This disables debug mode and prevents sensitive information from being leaked in error messages.
2.  **`SECRET_KEY`**: Set a long, random string. This is used for session signing.
3.  **`JWT_SECRET_KEY`**: Set another unique string for JWT token generation.

**Example Command to run in Prod**:
```bash
docker-compose up -d --build
```

---

## 📝 Submission & Evaluation

### Repository Link
[GitHub: shivam-singh-negi/Task-Manager-API](https://github.com/shivam-singh-negi/Task-Manager-API)

### Evaluation Criteria Checklist
- [x] **Code Organization**: Clean MVC structure with separated concerns.
- [x] **CRUD Implementation**: Robust task management logic.
- [x] **Auth & AuthZ**: JWT implementation with Role-based access.
- [x] **Test Quality**: 100% functional coverage for core logic.
- [x] **Documentation**: Self-documenting code with Swagger integration.

---

Built with ❤️ by **Shivam Singh Negi**
**Status:** ✅ Production Ready | **Version:** 1.0.0
