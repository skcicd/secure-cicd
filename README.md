# Secure Flask Application

## Overview
This is a **very secure Flask application** built as part of a DevSecOps project. It demonstrates modern web security practices while providing core functionality like user registration, login, and a weather-checking feature. The application is designed with simplicity and security in mind, making it an ideal example for deploying secure web applications.

---

## Features

### **Core Functionality**
1. **User Registration**
   - Users can register securely by providing a username and password.
   - Passwords are hashed using `pbkdf2:sha256` for secure storage.

2. **User Login**
   - Registered users can log in with their credentials.
   - Sessions are managed securely to track authenticated users.

3. **Weather Checker**
   - Logged-in users can check the current weather in any city.
   - Integrates with the OpenWeatherMap API to fetch real-time weather data.

4. **Logout**
   - Users can log out, clearing their session securely.

---

## Security Features

1. **Password Security**
   - Passwords are stored securely using `pbkdf2:sha256` hashing with salting.
   - Plaintext passwords are never stored.

2. **Session Management**
   - Flask's `session` is used to manage user authentication.
   - A strong `SECRET_KEY` ensures session integrity.
   - Sessions are configured to be HTTP-only and secure.

3. **Rate Limiting**
   - Rate limiting is enforced using `Flask-Limiter` to prevent brute-force attacks:
     - `/register`: 5 requests per minute per IP.
     - `/login`: 10 requests per minute per IP.

4. **TLS/HTTPS**
   - The app is configured to use TLS, ensuring all communication between the client and server is encrypted.

5. **Input Validation**
   - User inputs (e.g., username, password, city name) are sanitized and validated to prevent injection attacks.

6. **Content Security Policy (CSP)**
   - HTTP headers enforce a strict Content Security Policy to mitigate XSS attacks.

7. **Error Handling**
   - Graceful error handling prevents information leakage.
   - Detailed errors are logged server-side but not exposed to users.

8. **Environment Variables**
   - Sensitive information like `SECRET_KEY` and `OPENWEATHER_API_KEY` is stored securely in `.env` files and loaded using `python-dotenv`.

---

## Application Structure
```
secure_flask_app/
├── app/
│   ├── __init__.py        # Flask app factory and initialization
│   ├── routes.py          # Application routes and logic
│   ├── models.py          # User model and database logic
│   ├── utils.py           # Reusable utilities (e.g., login_required)
│   ├── templates/         # HTML templates
│   │   ├── index.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── weather.html
│   └── static/            # Static assets (e.g., favicon.ico)
├── config.py              # App configuration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── app.db                 # SQLite database
└── run.py                 # Application entry point
```

---

## Installation

### **Prerequisites**
- Python 3.9+
- Pip
- A free OpenWeatherMap API key

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/secure-flask-app.git
   cd secure-flask-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```plaintext
   SECRET_KEY=your-very-secure-key
   OPENWEATHER_API_KEY=your-openweather-api-key
   ```

5. Initialize the database:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. Run the application:
   ```bash
   python run.py
   ```

7. Access the app at `http://127.0.0.1:5000`.

---

## Deployment
- The app can be deployed securely using **Nginx** or **Apache** as a reverse proxy.
- Use **Gunicorn** or **uWSGI** for running the Flask app in production.
- Store sensitive keys securely using AWS Secrets Manager or similar tools.

---

## License
This project is licensed under the MIT License.

