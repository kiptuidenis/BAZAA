from rest_framework import serializers
from .models import STKRequest, STKCallback


class STKRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = STKRequest
        fields = ['id', 'user', 'phone', 'amount', 'checkout_request_id', 'merchant_request_id', 'response_code', 'response_description', 'timestamp']
        read_only_fields = ['id', 'checkout_request_id', 'merchant_request_id', 'response_code', 'response_description', 'timestamp']


class STKCallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = STKCallback
        fields = ['id', 'stk_request', 'result_code', 'result_desc', 'mpesa_receipt_number', 'amount', 'phone', 'transaction_date', 'created_at']
        read_only_fields = ['id', 'stk_request', 'created_at']
