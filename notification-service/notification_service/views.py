from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import pika
import json

from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Notification.objects.filter(user_id=user_id).order_by('-created_at')
        return Notification.objects.none()

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        notification_ids = request.data.get('notification_ids', [])
        Notification.objects.filter(id__in=notification_ids).update(is_read=True)
        return Response({'status': 'success'})

    @action(detail=False, methods=['post'])
    def send_notification(self, request):
        try:
            user_id = request.data.get('user_id')
            notification_type = request.data.get('notification_type')
            title = request.data.get('title')
            message = request.data.get('message')

            # Create notification in database
            notification = Notification.objects.create(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message
            )

            # Get user's notification preferences
            preferences = NotificationPreference.objects.get(user_id=user_id)

            # Send to message queue for processing
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
            )
            channel = connection.channel()
            channel.queue_declare(queue='notifications')

            notification_data = {
                'notification_id': notification.id,
                'user_id': user_id,
                'notification_type': notification_type,
                'title': title,
                'message': message,
                'preferences': {
                    'email': preferences.email_notifications,
                    'sms': preferences.sms_notifications,
                    'push': preferences.push_notifications
                }
            }

            channel.basic_publish(
                exchange='',
                routing_key='notifications',
                body=json.dumps(notification_data)
            )
            connection.close()

            return Response({
                'status': 'success',
                'message': 'Notification sent successfully',
                'data': self.get_serializer(notification).data
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return NotificationPreference.objects.filter(user_id=user_id)
        return NotificationPreference.objects.none() 