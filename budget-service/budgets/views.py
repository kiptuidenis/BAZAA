from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import date
import calendar

from .models import DailyBudget, MonthlyBudget, Transaction
from .serializers import (
    DailyBudgetSerializer,
    MonthlyBudgetSerializer,
    TransactionSerializer,
)


class DailyBudgetViewSet(viewsets.ModelViewSet):
    """
    Create, list, update, delete daily budgets. Automatically updates the monthly budget.
    """
    serializer_class = DailyBudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyBudget.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        self._update_monthly_budget()

    def perform_update(self, serializer):
        serializer.save()
        self._update_monthly_budget()

    def perform_destroy(self, instance):
        instance.delete()
        self._update_monthly_budget()

    def _update_monthly_budget(self):
        # sum up all daily budgets for user
        budgets = DailyBudget.objects.filter(user_id=self.request.user.id)
        total_daily = sum(b.amount for b in budgets)
        today = date.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        remaining_days = days_in_month - today.day + 1
        total_amount = total_daily * remaining_days
        # update or create monthly budget
        MonthlyBudget.objects.update_or_create(
            user_id=self.request.user.id,
            defaults={
                'total_amount': total_amount,
                'locked_amount': total_amount,
            }
        )


class MonthlyBudgetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve the current monthly budget for the authenticated user.
    """
    serializer_class = MonthlyBudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MonthlyBudget.objects.filter(user_id=self.request.user.id)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List all deposit and disbursement transactions for the user.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user.id).order_by('-timestamp')
