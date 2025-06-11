from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('deposit', 'Deposit'),
        ('disbursement', 'Disbursement'),
        ('budget_created', 'Budget Created'),
        ('budget_updated', 'Budget Updated'),
        ('system', 'System Notification'),
    )

    user_id = models.IntegerField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.title}"

class NotificationPreference(models.Model):
    user_id = models.IntegerField(unique=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification Preferences for User {self.user_id}" 