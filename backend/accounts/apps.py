from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError
import sys

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Avoid running during tests or migrations
        if 'makemigrations' in sys.argv or 'migrate' in sys.argv or 'test' in sys.argv:
            return

        try:
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                print("🚨 No superuser found. Creating default superuser...")
                User.objects.create_superuser(
                    email='admin@example.com',
                    username='admin',  
                    full_name='Administrator',
                    password='admin123'
                )
        except (OperationalError, ProgrammingError):
            # DB might not be ready yet
            pass
