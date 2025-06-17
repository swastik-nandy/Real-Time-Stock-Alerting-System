from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'target_price', 'is_triggered', 'created_at', 'triggered_at')
    search_fields = ('user__username', 'stock__symbol')
    list_filter = ('is_triggered', 'created_at')
    ordering = ('-created_at',)
