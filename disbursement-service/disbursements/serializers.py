from rest_framework import serializers
from .models import DisbursementSchedule, Disbursement

class DisbursementScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisbursementSchedule
        fields = '__all__'

class DisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disbursement
        fields = '__all__' 