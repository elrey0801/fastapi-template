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

## ✍️ Author

**elrey0801**