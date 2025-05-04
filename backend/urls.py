from django.contrib import admin
from django.urls import path, include
from .views import homepage_view


urlpatterns = [
    path('', homepage_view),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),


]
