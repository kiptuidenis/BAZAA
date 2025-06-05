from django.contrib import admin
from .models import DailyBudget, MonthlyBudget, Transaction

@admin.register(DailyBudget)
class DailyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'amount', 'created_at')
    list_filter = ('user_id',)

@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'total_amount', 'locked_amount', 'created_at')
    list_filter = ('user_id',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'amount', 'transaction_type', 'timestamp', 'reference')
    list_filter = ('transaction_type', 'user_id')
