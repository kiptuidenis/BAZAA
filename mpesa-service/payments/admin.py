from django.contrib import admin
from .models import STKPushRequest

@admin.register(STKPushRequest)
class STKPushRequestAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('phone_number', 'checkout_request_id', 'receipt_number')
    readonly_fields = (
        'checkout_request_id', 'merchant_request_id', 
        'response_code', 'response_description',
        'result_code', 'result_description',
        'receipt_number', 'created_at', 'updated_at'
    )
    ordering = ('-created_at',)
