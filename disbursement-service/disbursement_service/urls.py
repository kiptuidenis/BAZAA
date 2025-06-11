from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from disbursements.views import DisbursementScheduleViewSet, DisbursementViewSet

router = DefaultRouter()
router.register(r'schedules', DisbursementScheduleViewSet, basename='schedule')
router.register(r'disbursements', DisbursementViewSet, basename='disbursement')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] 