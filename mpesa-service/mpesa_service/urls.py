# URL configuration for mpesa_service
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mpesa/', include('payments.urls')),
]
