from django.db import models

class STKPushRequest(models.Model):
    """Represents an MPESA STK Push transaction request and its result."""
    user_id = models.IntegerField(help_text='ID of the user initiating the request')
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    response_code = models.CharField(max_length=10, blank=True, null=True)
    response_description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_description = models.CharField(max_length=255, blank=True, null=True)
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"STKPush {self.checkout_request_id} - {self.status}"
