from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import requests
import json

from .models import DisbursementSchedule, Disbursement
from .serializers import DisbursementScheduleSerializer, DisbursementSerializer

class DisbursementScheduleViewSet(viewsets.ModelViewSet):
    queryset = DisbursementSchedule.objects.all()
    serializer_class = DisbursementScheduleSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return DisbursementSchedule.objects.filter(user_id=user_id)
        return DisbursementSchedule.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            daily_amount = request.data.get('daily_amount')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            # Create schedule
            schedule = DisbursementSchedule.objects.create(
                user_id=user_id,
                daily_amount=daily_amount,
                start_date=start_date,
                end_date=end_date
            )

            # Create initial disbursements
            current_date = timezone.now().date()
            while current_date <= end_date:
                if current_date >= start_date:
                    Disbursement.objects.create(
                        user_id=user_id,
                        amount=daily_amount,
                        schedule=schedule,
                        scheduled_for=timezone.make_aware(
                            timezone.datetime.combine(current_date, timezone.time(8, 0))  # 8 AM
                        )
                    )
                current_date += timedelta(days=1)

            return Response({
                'status': 'success',
                'message': 'Disbursement schedule created successfully',
                'data': self.get_serializer(schedule).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisbursementViewSet(viewsets.ModelViewSet):
    queryset = Disbursement.objects.all()
    serializer_class = DisbursementSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Disbursement.objects.filter(user_id=user_id).order_by('-scheduled_for')
        return Disbursement.objects.none()

    @action(detail=False, methods=['post'])
    def process_pending(self, request):
        """Process all pending disbursements that are due"""
        try:
            now = timezone.now()
            pending_disbursements = Disbursement.objects.filter(
                status='pending',
                scheduled_for__lte=now
            )

            for disbursement in pending_disbursements:
                try:
                    # Mark as processing
                    disbursement.mark_as_processing()

                    # Call MPESA API to initiate disbursement
                    response = requests.post(
                        'http://mpesa-service:8003/api/mpesa/disburse/',
                        json={
                            'user_id': disbursement.user_id,
                            'amount': float(disbursement.amount),
                            'phone_number': f"254{disbursement.user_id}"  # Assuming user_id is the phone number
                        }
                    )

                    if response.status_code == 200:
                        response_data = response.json()
                        disbursement.mark_as_completed(response_data['transaction_id'])
                    else:
                        disbursement.mark_as_failed(response.json().get('message', 'Unknown error'))

                except Exception as e:
                    disbursement.mark_as_failed(str(e))

            return Response({
                'status': 'success',
                'message': f'Processed {pending_disbursements.count()} disbursements'
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 