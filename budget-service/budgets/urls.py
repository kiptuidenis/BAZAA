from rest_framework.routers import DefaultRouter
from .views import DailyBudgetViewSet, MonthlyBudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'daily', DailyBudgetViewSet, basename='dailybudget')
router.register(r'monthly', MonthlyBudgetViewSet, basename='monthlybudget')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
