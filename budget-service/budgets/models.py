from django.db import models
import datetime
import calendar


class DailyBudget(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - {self.name}: {self.amount}"


class MonthlyBudget(models.Model):
    user_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    locked_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MonthlyBudget User {self.user_id}: {self.locked_amount}/{self.total_amount}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('disbursement', 'Disbursement'),
    )
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type.title()} of {self.amount} for User {self.user_id}"
