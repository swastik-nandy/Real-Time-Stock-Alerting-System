from django.contrib import admin
from django.urls import path, include
from .views import homepage_view
from django.conf import settings
from django.conf.urls.static import static
from stocks.health import ping_view

urlpatterns = [
    path('', homepage_view),
    path('admin/', admin.site.urls),

    # API routes from your real apps
    path('ping/', ping_view),
    path('api/accounts/', include('accounts.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/stocks/', include('stocks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
