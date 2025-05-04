from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from alerts.models import Alert

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'full_name', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')  # Because we use email as login now

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('No user with this email exists.')
        return email

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['stock', 'target_price', 'condition']