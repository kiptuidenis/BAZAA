from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
import requests
import uuid

from .models import STKRequest, STKCallback
from .serializers import STKRequestSerializer, STKCallbackSerializer

User = get_user_model()


class STKPushView(APIView):
    """Initiate MPESA STK Push"""

    def post(self, request, *args, **kwargs):
        user = request.user
        phone = request.data.get('phone', getattr(user, 'mpesa_phone', None))
        amount = request.data.get('amount')
        if not phone or not amount:
            return Response({'detail': 'phone and amount required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create STKRequest
        checkout_request_id = str(uuid.uuid4())
        stk_req = STKRequest.objects.create(
            user=user,
            phone=phone,
            amount=amount,
            checkout_request_id=checkout_request_id
        )

        # Build payload (simulated or real)
        payload = {
            'BusinessShortCode': settings.MPESA_SHORTCODE,
            'Password': settings.MPESA_PASSWORD,
            'Timestamp': timezone.now().strftime('%Y%m%d%H%M%S'),
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone,
            'PartyB': settings.MPESA_SHORTCODE,
            'PhoneNumber': phone,
            'CallBackURL': settings.MPESA_CALLBACK_URL,
            'AccountReference': str(user.id),
            'TransactionDesc': 'BAZAA Deposit'
        }
        try:
            resp = requests.post(settings.MPESA_STK_PUSH_URL, json=payload)
            data = resp.json()
            stk_req.merchant_request_id = data.get('MerchantRequestID')
            stk_req.response_code = data.get('ResponseCode')
            stk_req.response_description = data.get('ResponseDescription')
            stk_req.save()
            return Response({'checkout_request_id': checkout_request_id}, status=status.HTTP_200_OK)
        except Exception as e:
            stk_req.response_description = str(e)
            stk_req.save()
            return Response({'detail': 'MPESA request failed'}, status=status.HTTP_502_BAD_GATEWAY)


class STKCallbackView(APIView):
    """Receive MPESA STK Push callback"""
    authentication_classes = []  # allow external callbacks
    permission_classes = []

    def post(self, request, *args, **kwargs):
        body = request.data.get('Body', {})
        result = body.get('stkCallback', {})
        checkout_request_id = result.get('CheckoutRequestID')
        if not checkout_request_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            stk_req = STKRequest.objects.get(checkout_request_id=checkout_request_id)
        except STKRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # parse metadata items
        items = result.get('CallbackMetadata', {}).get('Item', [])
        amount = next((i['Value'] for i in items if i.get('Name') == 'Amount'), None)
        mpesa_receipt = next((i['Value'] for i in items if i.get('Name') == 'MpesaReceiptNumber'), None)
        phone = next((i['Value'] for i in items if i.get('Name') == 'PhoneNumber'), None)

        callback = STKCallback.objects.create(
            stk_request=stk_req,
            result_code=result.get('ResultCode'),
            result_desc=result.get('ResultDesc'),
            mpesa_receipt_number=mpesa_receipt or '',
            amount=amount or 0,
            phone=phone or '',
            transaction_date=timezone.now()
        )
        return Response({'detail': 'callback received'}, status=status.HTTP_200_OK)
