from django.db import models

class FetchedStock(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.current_price}"
