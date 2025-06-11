from django.db import models
from django.utils import timezone

class DisbursementSchedule(models.Model):
    """Schedule for daily disbursements"""
    user_id = models.IntegerField()
    daily_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Disbursement Schedule for User {self.user_id}"

class Disbursement(models.Model):
    """Record of actual disbursements"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    schedule = models.ForeignKey(DisbursementSchedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mpesa_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    scheduled_for = models.DateTimeField()
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Disbursement {self.id} - {self.status}"

    def mark_as_processing(self):
        self.status = 'processing'
        self.save()

    def mark_as_completed(self, mpesa_transaction_id):
        self.status = 'completed'
        self.mpesa_transaction_id = mpesa_transaction_id
        self.processed_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.processed_at = timezone.now()
        self.save() 