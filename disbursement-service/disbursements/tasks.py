from celery import shared_task
from django.conf import settings
from django.utils import timezone
import requests
import logging

from .models import Disbursement

logger = logging.getLogger(__name__)

@shared_task
def process_daily_disbursements():
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
                    f'{settings.MPESA_SERVICE_URL}/api/mpesa/disburse/',
                    json={
                        'user_id': disbursement.user_id,
                        'amount': float(disbursement.amount),
                        'phone_number': f"254{disbursement.user_id}"  # Assuming user_id is the phone number
                    }
                )

                if response.status_code == 200:
                    response_data = response.json()
                    disbursement.mark_as_completed(response_data['transaction_id'])
                    
                    # Notify user of successful disbursement
                    requests.post(
                        f'{settings.NOTIFICATION_SERVICE_URL}/api/notifications/send/',
                        json={
                            'user_id': disbursement.user_id,
                            'notification_type': 'disbursement',
                            'title': 'Daily Disbursement Successful',
                            'message': f'Your daily disbursement of KES {disbursement.amount} has been sent to your MPESA account.'
                        }
                    )
                else:
                    error_message = response.json().get('message', 'Unknown error')
                    disbursement.mark_as_failed(error_message)
                    
                    # Notify user of failed disbursement
                    requests.post(
                        f'{settings.NOTIFICATION_SERVICE_URL}/api/notifications/send/',
                        json={
                            'user_id': disbursement.user_id,
                            'notification_type': 'disbursement',
                            'title': 'Daily Disbursement Failed',
                            'message': f'Failed to process your daily disbursement of KES {disbursement.amount}. Error: {error_message}'
                        }
                    )

            except Exception as e:
                logger.error(f"Error processing disbursement {disbursement.id}: {str(e)}")
                disbursement.mark_as_failed(str(e))

        return f'Processed {pending_disbursements.count()} disbursements'

    except Exception as e:
        logger.error(f"Error in process_daily_disbursements: {str(e)}")
        raise 