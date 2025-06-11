"""Views for handling MPESA STK Push requests and callbacks."""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
import json

from .models import STKPushRequest
from .serializers import (
    STKPushRequestSerializer,
    STKCallbackSerializer,
    STKPushResultSerializer
)

class MPESAServiceViewSet(viewsets.ModelViewSet):
    queryset = STKPushRequest.objects.all()
    serializer_class = STKPushRequestSerializer

    def get_access_token(self):
        """Get MPESA API access token"""
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        auth_url = settings.MPESA_AUTH_URL

        response = requests.get(
            auth_url,
            auth=(consumer_key, consumer_secret)
        )
        return response.json()['access_token']

    @action(detail=False, methods=['post'])
    def initiate_stk_push(self, request):
        """Initiate STK Push request"""
        try:
            access_token = self.get_access_token()
            phone_number = request.data.get('phone_number')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')

            # Format phone number (remove leading 0 and add country code)
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            payload = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": settings.MPESA_PASSWORD,
                "Timestamp": settings.MPESA_TIMESTAMP,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": settings.MPESA_SHORTCODE,
                "PhoneNumber": phone_number,
                "CallBackURL": settings.MPESA_CALLBACK_URL,
                "AccountReference": f"BAZAA_{user_id}",
                "TransactionDesc": "BAZAA Deposit"
            }

            response = requests.post(
                settings.MPESA_STK_PUSH_URL,
                headers=headers,
                json=payload
            )
            response_data = response.json()

            if response.status_code == 200:
                stk_push = STKPushRequest.objects.create(
                    user_id=user_id,
                    phone_number=phone_number,
                    amount=amount,
                    checkout_request_id=response_data['CheckoutRequestID'],
                    merchant_request_id=response_data['MerchantRequestID'],
                    response_code=response_data['ResponseCode'],
                    response_description=response_data['ResponseDescription']
                )
                return Response({
                    'status': 'success',
                    'message': 'STK Push initiated successfully',
                    'data': self.get_serializer(stk_push).data
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Failed to initiate STK Push',
                    'error': response_data
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def stk_push_callback(self, request):
        """Handle STK Push callback"""
        try:
            callback_data = request.data
            checkout_request_id = callback_data['Body']['stkCallback']['CheckoutRequestID']
            result_code = callback_data['Body']['stkCallback']['ResultCode']
            result_description = callback_data['Body']['stkCallback']['ResultDesc']

            stk_push = STKPushRequest.objects.get(checkout_request_id=checkout_request_id)
            
            if result_code == 0:
                # Transaction successful
                callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']['Item']
                receipt_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber')
                
                stk_push.status = 'SUCCESS'
                stk_push.result_code = result_code
                stk_push.result_description = result_description
                stk_push.receipt_number = receipt_number
                stk_push.save()

                # TODO: Trigger notification service
                # TODO: Update user's balance in budget service

            else:
                stk_push.status = 'FAILED'
                stk_push.result_code = result_code
                stk_push.result_description = result_description
                stk_push.save()

            return Response({'status': 'success'})

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
