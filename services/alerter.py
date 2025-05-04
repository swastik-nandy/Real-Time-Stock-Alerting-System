import time
import os
import sys
import django
import json
from django.core.mail import send_mail
from dotenv import load_dotenv
from pathlib import Path
from pywebpush import webpush, WebPushException

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
from accounts.models import PushSubscription
from django.utils import timezone


# === ALERT CHECKER LOOP ===

def check_and_notify_alerts():
    while True:
        # Get all untriggered alerts with related stock and user info
        alerts = Alert.objects.select_related("user", "stock").filter(is_triggered=False)

        for alert in alerts:
            stock = alert.stock
            user = alert.user
            current_price = stock.latest_price
            target = alert.target_price
            condition = alert.condition

            # === Check if alert is triggered ===
            if condition == "above" and current_price >= target:
                subject = f"Stock Alert: {stock.symbol} reached {current_price}"
                message = f"The price of {stock.symbol} is now {current_price}, which is above your target of {target}."
            elif condition == "below" and current_price <= target:
                subject = f"Stock Alert: {stock.symbol} dropped to {current_price}"
                message = f"The price of {stock.symbol} is now {current_price}, which is below your target of {target}."
            else:
                continue  # Skip if not triggered

            # === Send Email Notification ===
            try:
                send_mail(
                    subject,
                    message,
                    os.getenv("ALERT_FROM_EMAIL"),
                    [user.email],
                    fail_silently=True,
                )
                print(f"[EMAIL SENT] To: {user.email} | {stock.symbol} at {current_price}")
            except Exception as e:
                print(f"[ERROR] Sending email failed for {user.email}: {e}")

            # === Send Push Notification (JSON format for service worker) ===
            subscriptions = PushSubscription.objects.filter(user=user)
            print(f"[DEBUG] Found {subscriptions.count()} subscriptions for {user.email}")

            for sub in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": sub.endpoint,
                            "keys": {
                                "auth": sub.auth,
                                "p256dh": sub.p256dh,
                            }
                        },
                        data=json.dumps({  # 👈 sending as structured JSON
                            "title": subject,
                            "message": message
                        }),
                        vapid_private_key=os.getenv("VAPID_PRIVATE_KEY"),
                        vapid_claims={"sub": "mailto:" + os.getenv("ALERT_FROM_EMAIL")}
                    )
                    print(f"[PUSH SENT] To: {user.email} | {stock.symbol} at {current_price}")
                except WebPushException as e:
                    print(f"[ERROR] Push failed for {user.email}: {e}")

            # === Delete Alert After Processing ===
            alert.delete()
            print(f"[ALERT REMOVED] {user.email} | {stock.symbol} ({condition})")

        # Sleep 1 second before checking again
        time.sleep(1)


# === ENTRY POINT ===
if __name__ == "__main__":
    check_and_notify_alerts()
