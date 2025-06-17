from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # AAPL, GOOGL, TSLA
    company_name = models.CharField(max_length=100)
    latest_price = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)  # Auto update when price updates

    def __str__(self):
        return f"{self.symbol} - {self.company_name}"


class StockPriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['stock', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.stock.symbol} @ {self.price} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
