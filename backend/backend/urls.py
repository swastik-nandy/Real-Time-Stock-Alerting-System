from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from .views import homepage_view
from stocks.health import ping_view

# ✅ Health check endpoint for Render
def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)

urlpatterns = [
    path('', homepage_view),
    path('admin/', admin.site.urls),

    # Health & Ping
    path('health/', health_check),
    path('ping/', ping_view),

    # API routes
    path('api/accounts/', include('accounts.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/stocks/', include('stocks.urls')),
]

# ✅ Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
