from django.urls import path
from .views import STKPushView, STKPushCallbackView

urlpatterns = [
    path('stkpush/', STKPushView.as_view(), name='stk-push'),
    path('stkpush/callback/', STKPushCallbackView.as_view(), name='stk-callback'),
]
