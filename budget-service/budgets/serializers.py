from rest_framework import serializers
from .models import DailyBudget, MonthlyBudget, Transaction


class DailyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBudget
        fields = ['id', 'name', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = ['id', 'total_amount', 'locked_amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'timestamp', 'reference']
        read_only_fields = ['id', 'timestamp', 'transaction_type', 'reference']
