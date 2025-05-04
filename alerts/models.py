from django.db import models
from django.contrib.auth import get_user_model
from stocks.models import Stock

User = get_user_model()

class Alert(models.Model):
    CONDITION_CHOICES = (
        ('above', 'Above Target Price'),
        ('below', 'Below Target Price'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='alerts')
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='above')
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return f"Alert({self.user.username} - {self.stock.symbol} @ {self.target_price} [{self.condition}])"