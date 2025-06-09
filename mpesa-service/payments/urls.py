from django.urls import path
from .views import STKPushView, STKCallbackView

urlpatterns = [
    path('stkpush/', STKPushView.as_view(), name='stkpush'),
    path('callback/', STKCallbackView.as_view(), name='stkpush_callback'),
]
