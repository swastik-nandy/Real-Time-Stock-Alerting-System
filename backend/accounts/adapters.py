from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Extract Google profile info
        email = data.get('email')
        full_name = data.get('name') or f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        username = email.split('@')[0] if email else get_random_string(10)

        # Assign data to your CustomUser fields
        user.email = email
        user.full_name = full_name
        user.username = username

        # Generate and hash a random password
        random_password = get_random_string(length=12)
        user.set_password(random_password)

        return user

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        try:
            user = User.objects.get(email=email)
            if user.is_superuser or user.is_staff:
                raise PermissionDenied("Admin users cannot login with Google.")
        except User.DoesNotExist:
            pass  # New user, proceed as normal
