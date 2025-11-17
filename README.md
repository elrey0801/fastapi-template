# FastAPI Template ⚡

A production-ready FastAPI template with modern architecture, focusing on performance, security, and scalability.

## 📜 About the Template

This template provides a robust and well-structured foundation for FastAPI projects, implementing best practices and essential features for modern web applications:

* **Database (DB):** MySQL with **asynchronous (async) connection** using `aiomysql` and SQLAlchemy for optimized I/O performance and scalability.
* **Authentication:** **JWT (JSON Web Token)** authentication with access/refresh token pair. Each user has a unique private key for enhanced security.
* **Exception Handling:** Centralized exception handler with standardized error codes and responses.
* **Architecture:** Clean architecture with separation of concerns (Controller → Service → Model).
* **Middleware:** Cookie-based authentication middleware with role-based access control.
* **Configuration:** Environment-based configuration using Pydantic Settings.
* **Logging:** Structured logging with ColorLog for better debugging.

---

## 🛠️ Key Features

| Feature | Description |
| :--- | :--- |
| **MySQL Async** | Asynchronous DB operations with SQLAlchemy for better performance |
| **JWT Authentication** | Dual-token system (access + refresh) with per-user encryption keys |
| **Exception Handling** | Centralized error handling with custom error codes and messages |
| **Role-Based Access** | Built-in role system (Admin, User, Trial User) with priority levels |
| **CORS Support** | Configurable CORS middleware for cross-origin requests |
| **Environment Config** | Type-safe configuration management with Pydantic |
| **Cookie Middleware** | Secure cookie-based authentication with automatic token refresh |
| **Logging System** | Structured logging with color-coded output for development |
| **Password Hashing** | Bcrypt password hashing for secure credential storage |

---

## 📁 Project Structure

```
src/
├── app.py                      # FastAPI application setup and configuration
├── server.py                   # Application entry point
├── .env                        # Environment variables (not in git)
│
├── config/                     # Configuration modules
│   ├── __init__.py
│   ├── async_mysql.py         # MySQL async connection setup
│   ├── env_config.py          # Environment settings (Pydantic)
│   └── logger.py              # Logging configuration
│
├── controller/                 # Request handlers (business logic)
│   ├── auth_controller.py     # Authentication operations
│   └── user_controller.py     # User management operations
│
├── service/                    # Data access layer
│   ├── service.py             # Base service class
│   ├── token_service.py       # Token database operations
│   └── user_service.py        # User database operations
│
├── model/                      # Database models (SQLAlchemy)
│   ├── user.py                # User model with Role enum
│   └── token.py               # Token model (access/refresh)
│
├── dto/                        # Data Transfer Objects (Pydantic)
│   ├── base_response.py       # Standard API response format
│   ├── token_dto.py           # Token-related DTOs
│   └── user_dto.py            # User-related DTOs
│
├── exception/                  # Error handling
│   ├── app_exception.py       # Custom exception class
│   ├── error_code.py          # Error code definitions
│   └── global_exception_handler.py  # Global exception handler
│
├── middleware/                 # Custom middleware
│   └── verify_cookie.py       # Cookie authentication middleware
│
└── util/                       # Utility functions
    └── cookies.py             # Cookie management utilities
```

---

## 🚀 Tech Stack

- **Framework:** FastAPI 0.116.1
- **Database:** MySQL with aiomysql (async) + SQLAlchemy
- **Authentication:** PyJWT 2.10.1
- **Password Hashing:** bcrypt 4.3.0
- **Validation:** Pydantic 2.11.5
- **Server:** Uvicorn with multi-worker support
- **Logging:** ColorLog 6.9.0
- **Environment:** python-dotenv 1.1.0
- **CORS:** FastAPI CORS Middleware

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- MySQL Server
- pip or conda

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/elrey0801/fastapi-template.git
   cd fastapi-template
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   
   Create a `.env` file in the `src/` directory:
   ```bash
   cp src/.env.example src/.env  # If example exists, or create manually
   ```

   Edit `src/.env` with your configuration:
   ```env
   # Application Settings
   PROJECT_NAME=YourProjectName
   APP_WORKERS=1
   PORT=9999
   HOST=0.0.0.0
   ENV=dev
   
   # Database Configuration
   DB_USERNAME=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost:3306
   DB_NAME=your_database_name
   
   # CORS Settings
   ORIGINS=http://localhost:3000,http://localhost:5173
   
   # JWT Token Settings (in seconds)
   ACCESS_TOKEN_MAX_AGE=3600        # 1 hour
   REFRESH_TOKEN_MAX_AGE=259200     # 3 days
   
   # Feature Flags
   OPEN_USER_REGISTRATION=1         # 1=enabled, 0=disabled
   PRODUCTION_MODE=0                # 1=production, 0=development
   ```

5. **Run database migrations:**
   
   The template automatically creates tables on startup via SQLAlchemy:
   ```python
   DBMySQL.Base.metadata.create_all(bind=DBMySQL._sync_engine)
   ```

---

## 🏃 Running the Application

### Development Mode

```bash
cd src
python server.py
```

Or with uvicorn directly:
```bash
cd src
uvicorn app:app --host 0.0.0.0 --port 9999 --reload
```

### Production Mode

Set `PRODUCTION_MODE=1` in `.env` and configure workers:

```bash
cd src
python server.py
```

The server will run with the number of workers specified in `APP_WORKERS`.

---

## 🔐 Authentication Flow

This template implements a **dual-token authentication system**:

1. **Access Token**: Short-lived token (default: 1 hour) for API requests
2. **Refresh Token**: Long-lived token (default: 3 days) for obtaining new access tokens

### Token Storage
- Tokens are stored in **HTTP-only cookies** for security
- Each user has a unique `private_key` for token encryption
- Token pairs are tracked in the database

### Role-Based Access Control
Three built-in roles with priority levels:
- **Admin** (priority: 3) - Full access
- **User** (priority: 2) - Standard access  
- **Trial User** (priority: 1) - Limited access

Use the `VerifyCookies` middleware to protect routes:
```python
from middleware import VerifyCookies
from model import Role

@app.get("/protected")
async def protected_route(user_data = Depends(VerifyCookies(minimum_role=Role.USER))):
    return {"user": user_data}
```

---

## ⚙️ Configuration

All settings are managed through `src/config/env_config.py` using Pydantic Settings:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROJECT_NAME` | str | "PDDA2-API" | Application name |
| `APP_WORKERS` | int | 1 | Number of Uvicorn workers |
| `DB_USERNAME` | str | - | MySQL username |
| `DB_PASSWORD` | str | - | MySQL password |
| `DB_HOST` | str | - | MySQL host:port |
| `DB_NAME` | str | - | Database name |
| `PORT` | int | 8888 | Server port |
| `HOST` | str | "0.0.0.0" | Server host |
| `ENV` | str | "dev" | Environment (dev/prod) |
| `ORIGINS` | str | "*" | Allowed CORS origins (comma-separated) |
| `ACCESS_TOKEN_MAX_AGE` | int | 3600 | Access token lifetime (seconds) |
| `REFRESH_TOKEN_MAX_AGE` | int | 604800 | Refresh token lifetime (seconds) |
| `OPEN_USER_REGISTRATION` | bool | false | Allow public user registration |
| `PRODUCTION_MODE` | bool | false | Enable production mode |

---

## 📝 Usage Example

### Creating Your First Router

```python
# In your new controller file
from fastapi import APIRouter, Depends
from middleware import VerifyCookies
from model import Role

router = APIRouter(prefix="/api/v1", tags=["Example"])

@router.get("/hello")
async def hello_world():
    return {"message": "Hello from FastAPI Template!"}

@router.get("/protected")
async def protected_route(user_data = Depends(VerifyCookies(minimum_role=Role.USER))):
    return {"user_id": user_data["user"].id}
```

### Adding to app.py

```python
from your_controller import router as your_router

app.include_router(your_router)
```

---

## 🧪 Error Handling

The template includes comprehensive error handling:

```python
from exception import AppException, ErrorCode

# Raise custom exceptions
raise AppException(
    error_code=ErrorCode.USER_NOT_FOUND,
    alt_message="Additional debug info",
    return_message="Custom user message"
)
```

Standard response format:
```json
{
  "code": 4002,
  "message": "User not found!",
  "data": null
}
```

---

## 🔒 Security Features

- ✅ Bcrypt password hashing
- ✅ Per-user JWT encryption keys
- ✅ HTTP-only cookies for token storage
- ✅ Role-based access control
- ✅ CORS configuration
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)

---

## 🛣️ Roadmap

This is a template - you can extend it with:

- [ ] API endpoints for your business logic
- [ ] File upload handling
- [ ] Email service integration
- [ ] Background tasks (Celery/APScheduler)
- [ ] Rate limiting
- [ ] API documentation (Swagger/ReDoc)
- [ ] Testing suite (pytest)
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 📄 License

This template is open source and available for use in your projects.

---

## ✍️ Author

**elrey0801**

---

## 🤝 Contributing

Feel free to fork this template and customize it for your needs. If you find bugs or have suggestions, please open an issue or submit a pull request!

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT.io](https://jwt.io/)