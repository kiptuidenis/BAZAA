from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/budget/', include('budget_management.urls')),
    path('api/mpesa/', include('mpesa_integration.urls')),
]
