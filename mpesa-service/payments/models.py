from django.db import models
from django.conf import settings
from django.utils import timezone


class STKRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    response_code = models.CharField(max_length=10, blank=True, null=True)
    response_description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"STKRequest {self.checkout_request_id} for user {self.user}"


class STKCallback(models.Model):
    stk_request = models.OneToOneField(STKRequest, on_delete=models.CASCADE)
    result_code = models.CharField(max_length=10)
    result_desc = models.CharField(max_length=255)
    mpesa_receipt_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone = models.CharField(max_length=20)
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"STKCallback {self.mpesa_receipt_number} ({self.result_code})"
