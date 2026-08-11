# API Endpoints Documentation

This document contains all the backend API endpoints grouped by their logical domains, making it easier to track and maintain requests and responses.

## Authentication Routes

*(Base URL depending on your app entry point, e.g., `/api/auth`)*

---

### 1. Sign Up
- **Endpoint**: `POST /sign-up`
- **Description**: Register a new user account.
- **Request Format**: `multipart/form-data`
  - `fullName` (string, required)
  - `email` (string, required)
  - `password` (string, required)
  - `avatar` (file, optional)
- **Responses**:
  - **201 Created** (Success)
    ```json
    {
      "status": "success",
      "message": "successful registration, check your email",
      "action": "verify_email"
    }
    ```
  - **400 Bad Request** (Email already exists, blocked, or unverified)

---

### 2. Sign In
- **Endpoint**: `POST /sign-in`
- **Description**: Authenticate a user and create a session.
- **Request Format**: `application/json`
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Responses**:
  - **200 OK** (Success)
    ```json
    {
      "status": "success",
      "message": "Logged in successfully",
      "data": {
        "_id": "user_id",
        "email": "user@example.com",
        "role": "User"
      }
    }
    ```
  - **401/403 Error** (Invalid credentials, unverified account, or blocked)

---

### 3. Verify Email
- **Endpoint**: `POST /verify-email`
- **Description**: Verify user's email using the code sent during signup.
- **Headers**: Requires authentication cookie (`Theta-Hack-Auth`).
- **Request Format**: `application/json`
  ```json
  {
    "code": "123456"
  }
  ```
- **Responses**:
  - **200 OK** (Success)
    ```json
    {
      "status": "success",
      "message": "Email verified successfully",
      "data": {
        "_id": "user_id",
        "email": "user@example.com",
        "role": "User",
        "status": "Active"
      }
    }
    ```
  - **400/404 Error** (Invalid code, already verified, or user not found)

---

### 4. Verify Me / Check Auth
- **Endpoints**: 
  - `GET /verify-me`
  - `GET /check-auth`
- **Description**: Get the current authenticated user's information.
- **Headers**: Requires authentication cookie (`Theta-Hack-Auth`).
- **Request Format**: None
- **Responses**:
  - **200 OK** (Success)
    ```json
    {
      "status": "success",
      "message": "User verified successfully",
      "data": {
        "user": {
          "_id": "user_id",
          "role": "User",
          "status": "Active",
          "email": "user@example.com",
          "fullName": "John Doe",
          "avatar": "url_to_image"
        }
      }
    }
    ```
  - **401 Unauthorized** (No valid token or unauthorized status)

---

### 5. Log Out
- **Endpoint**: `POST /log-out`
- **Description**: Revoke session(s) and clear the authentication cookie.
- **Headers**: Requires authentication cookie (`Theta-Hack-Auth`).
- **Query Parameters**: 
  - `target` (optional, default: `me`): Can be `me`, `all`, or `others`.
- **Request Format**: None
- **Responses**:
  - **200 OK** (Success)
    ```json
    {
      "status": "success",
      "message": "Logged out successfully"
    }
    ```
  - **400 Bad Request** (Invalid target)

---

## Models / Resources Routes (Future)

*(In the future, group endpoints that interact with specific models below. For example, `## User Routes`, `## Post Routes`, etc.)*
