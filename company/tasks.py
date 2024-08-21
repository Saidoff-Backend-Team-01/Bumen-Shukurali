from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from django.conf import settings
from pyfcm import FCMNotification

from account.models import User

from .models import Notification


@shared_task
def send_fcm_notification(notification_id: Notification):
    """
    Send push notification via FCM
    :param registration_ids: List of FCM registration tokens (device tokens)
    :param title: Notification title
    :param message: Notification body message
    :param data: Optional custom data to include in the notification
    :return: Response from FCM
    """
    push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
    notification = Notification.objects.filter(id=notification_id).first()
    if notification.is_all_users:
        user_device_ids = User.objects.all().values_list("device_id", flat=True)
        result = push_service.notify_multiple_devices(
            registration_ids=user_device_ids,
            message_title=notification.title,
            message_body=notification.message,
            data_message=notification.extra_data,
        )

    return result
