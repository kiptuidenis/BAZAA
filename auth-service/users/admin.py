from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('mpesa_phone', 'is_active', 'is_staff', 'created_at')
    ordering = ('mpesa_phone',)
    search_fields = ('mpesa_phone',)
