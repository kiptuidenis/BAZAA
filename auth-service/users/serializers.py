from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['mpesa_phone', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            mpesa_phone=validated_data['mpesa_phone'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    mpesa_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
