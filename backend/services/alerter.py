import time
import os
import sys
import django
from dotenv import load_dotenv
from pathlib import Path
from django.core.mail import send_mail

# === SETUP ===

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# === IMPORT MODELS ===

from alerts.models import Alert
from django.utils import timezone


# === ALERT CHECKER LOOP ===

def check_and_notify_alerts():
    while True:
        alerts = Alert.objects.select_related("user", "stock").filter(is_triggered=False)

        for alert in alerts:
            stock = alert.stock
            user = alert.user
            current_price = stock.latest_price
            target = alert.target_price
            condition = alert.condition

            if condition == "above" and current_price >= target:
                subject = f"Stock Alert: {stock.symbol} reached {current_price}"
                message = f"The price of {stock.symbol} is now {current_price}, which is above your target of {target}."
            elif condition == "below" and current_price <= target:
                subject = f"Stock Alert: {stock.symbol} dropped to {current_price}"
                message = f"The price of {stock.symbol} is now {current_price}, which is below your target of {target}."
            else:
                continue  # not triggered

            # === Send Email ===
            try:
                send_mail(
                    subject,
                    message,
                    os.getenv("ALERTS_FROM_EMAIL"),
                    [user.email],
                    fail_silently=True,
                )
                print(f"[EMAIL SENT] To: {user.email} | {stock.symbol} at {current_price}")
            except Exception as e:
                print(f"[ERROR] Sending email failed for {user.email}: {e}")

            # === Remove Alert ===
            alert.delete()
            print(f"[ALERT REMOVED] {user.email} | {stock.symbol} ({condition})")

        time.sleep(1)


# === ENTRY POINT ===
if __name__ == "__main__":
    check_and_notify_alerts()
