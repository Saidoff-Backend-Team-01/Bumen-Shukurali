import json
from datetime import datetime

from django.db.models.signals import post_save
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from .models import Notification


def post_save_notification_date(sender, instance: Notification, created, **kwargs):
    if created:
        user = instance.user
        if not instance.scheduled_date:
            current_time = datetime.utcnow()
            clocked_schedule = ClockedSchedule.objects.create(clocked_time=current_time)
        else:
            clocked_schedule = ClockedSchedule.objects.create(
                cloced_time=instance.scheduled_date
            )

        PeriodicTask.objects.create(
            name=f"Sending notifications to users: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            clocked=clocked_schedule,
            task="company.tasks.send_fcm_notification",
            enabled=True,
            one_off=True,
            kwargs=json.dumps({"notification_id": instance.id}),
        )


post_save.connect(post_save_notification_date, sender=Notification)
