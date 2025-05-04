from django import forms
from .models import Alert
from stocks.models import Stock

CONDITION_CHOICES = [
    ('above', 'Above Target Price'),
    ('below', 'Below Target Price'),
]

class AlertForm(forms.ModelForm):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all(), label="Select Stock")
    target_price = forms.DecimalField(max_digits=12, decimal_places=2, label="Target Price")
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, label="Condition")

    class Meta:
        model = Alert
        fields = ['stock', 'target_price', 'condition']