# 🧠 Real-Time Stock Predictor — Setup Instructions

This guide walks you through setting up and running the Real-Time Stock Predictor locally. It includes backend configuration, PostgreSQL setup, alert logic, and testing.

---

## 📦 1. Prerequisites

Make sure you have the following installed:

- Python 3.9+
- pip
- PostgreSQL
- Git
- Virtualenv (recommended)
- Optional: Docker (if running in container)

---

## 📁 2. Clone the Repository

```bash
git clone https://github.com/your-username/Real-Time-Stock-Predictor.git
cd Real-Time-Stock-Predictor
```

---

## 🌱 3. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate       # Linux/macOS
env\Scripts\activate          # Windows
```

---

## 📜 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 5. Configure PostgreSQL

### ➤ Step 1: Open PostgreSQL and Create a Database

Login via `psql`:

```bash
psql -U postgres
```

Create user and database:

```sql
CREATE DATABASE stock_db;
CREATE USER stock_user WITH PASSWORD 'your_password';
ALTER ROLE stock_user SET client_encoding TO 'utf8';
ALTER ROLE stock_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE stock_user SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE stock_db TO stock_user;
```

### ➤ Step 2: Add DB Credentials to `backend/settings.py`

Find the `DATABASES` section and configure like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stock_db',
        'USER': 'stock_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

*Do NOT put real credentials if committing. Use a `.env` file in production.*

---

## ⚙️ 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 🚀 7. Run the Server

```bash
python manage.py runserver
```

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 8. Test the API (Examples)

You can use Postman or curl to test:

### Register:

```bash
POST /register/
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "pass123"
}
```

### Login:

```bash
POST /login/
{
  "identifier": "testuser",   # or email
  "password": "pass123"
}
```

### Create Alert:

```bash
POST /create_alert/
{
  "stock": "AAPL",
  "target_price": 170.50,
  "condition": "greater"
}
```

---

## ⏰ 9. Run Stock Price Checker (Alert Trigger)

Manually run the fetcher script:

```bash
python script.py
```

This will:
- Fetch live prices
- Match against saved alerts
- Send notifications (e.g., console/email)

You can later add a cron job to automate this every 10 mins.

---

## 🧹 10. Optional Cleanup Tips

- Use `.env` + `python-decouple` to manage secrets.
- Use `django-cors-headers` if connecting frontend (e.g., React/Vue).
- Set up custom logs to monitor trigger outcomes.

---

## 📬 11. Contact & Troubleshooting

- App not connecting to DB? Recheck `settings.py` credentials.
- Alerts not firing? Make sure `script.py` is hitting alert logic correctly.
- Need advanced notifications? Expand the `notifications/` module with email/SMS integrations.

---

✅ **You’re now ready to test and improve your real-time stock predictor!**

