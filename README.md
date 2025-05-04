# 📈 Real-Time Stock Alerting System

A real-time stock alerting platform built with Django and PostgreSQL. It allows users to monitor live stock prices, define custom alerts, and get notified instantly via email and web push notifications. Features secure Google OAuth and OTP-based login, with a modular backend architecture and production-ready setup.

---

## 🚀 Features

| Category       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| 🔐 Auth         | Login via Google OAuth2 and custom email-password system with OTP          |
| 📊 Stocks       | Live price fetching via Finnhub API with periodic refreshing                |
| 📬 Alerts       | Define alerts like “AAPL > 150” and get notified instantly                  |
| 📢 Notifications| Email & web push (via `notifier.js`) triggered automatically                |
| ⚙️ Services     | Background scripts: `fetcher.py`, `alerter.py`              |
| 🧾 Admin Panel  | Django admin for user, alert, and stock management                          |

---

## 🧠 Tech Stack

| Layer        | Tools & Tech                    |
|--------------|----------------------------------|
| Backend      | Django 4.x (Python)             |
| Frontend     | HTML, CSS, Bootstrap, JS        |
| Database     | PostgreSQL                      |
| Auth         | Google OAuth2 + Email OTP       |
| API          | Finnhub Stock API               |
| Notification | SMTP (email) + Web Push         |
| Services     | Python background scripts       |

---

## 🧪 API Endpoints

> These endpoints are RESTful and follow secure routing conventions.

| Endpoint                          | Method | Description                                     |
|----------------------------------|--------|-------------------------------------------------|
| `/register/`                     | POST   | Register user with email, username & password   |
| `/login/`                        | POST   | Login via email or username                     |
| `/google/login/callback/`       | GET    | Google OAuth2 callback for login                |
| `/verify-otp/`                  | POST   | Verify OTP sent via email                       |
| `/reset-password/`              | POST   | Reset password after OTP verification           |
| `/api/stocks/`                  | GET    | Fetch list of stocks being monitored            |
| `/api/alerts/`                  | GET    | Get all alerts for current user                 |
| `/api/alerts/create/`           | POST   | Create a new stock price alert                  |
| `/api/alerts/delete/<id>/`      | DELETE | Delete a specific alert                         |
| `/api/usage/`                   | GET    | Get user’s usage stats (limits, pro status)     |

---

## 🧾 Project Structure

