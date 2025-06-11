import pika
import json
from django.conf import settings
from django.core.mail import send_mail
from .models import Notification

def process_notifications():
    """Process notifications from RabbitMQ queue"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD
            )
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='notifications')

    def callback(ch, method, properties, body):
        try:
            notification_data = json.loads(body)
            
            # Send email notification if enabled
            if notification_data['preferences']['email']:
                send_mail(
                    subject=notification_data['title'],
                    message=notification_data['message'],
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[f"user_{notification_data['user_id']}@example.com"],  # Replace with actual email
                    fail_silently=True
                )

            # TODO: Implement SMS notification
            if notification_data['preferences']['sms']:
                pass

            # TODO: Implement push notification
            if notification_data['preferences']['push']:
                pass

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"Error processing notification: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue='notifications',
        on_message_callback=callback
    )

    print('Started consuming notifications...')
    channel.start_consuming()

if __name__ == '__main__':
    process_notifications() 