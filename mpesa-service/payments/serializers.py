from rest_framework import serializers
from .models import STKPushRequest

class STKPushRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_phone_number(self, value):
        # Basic validation, can be expanded (e.g., regex for Safaricom numbers)
        if not value.startswith('254') or not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Phone number must be in the format 254xxxxxxxxx")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

class STKCallbackSerializer(serializers.Serializer):
    Body = serializers.JSONField()

    def validate_Body(self, value):
        stk_callback = value.get('stkCallback')
        if not stk_callback:
            raise serializers.ValidationError("Missing 'stkCallback' in Body")
        
        required_fields = ['MerchantRequestID', 'CheckoutRequestID', 'ResultCode']
        for field in required_fields:
            if field not in stk_callback:
                raise serializers.ValidationError(f"Missing '{field}' in stkCallback data")
        return value

class STKPushResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = STKPushRequest
        fields = '__all__'
        read_only_fields = ('user_id', 'created_at', 'updated_at')
