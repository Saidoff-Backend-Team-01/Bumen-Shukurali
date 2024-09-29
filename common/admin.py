from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Media

# from django.contrib import admin
# from django_celery_beat.models import (
#     PeriodicTask, CrontabSchedule, IntervalSchedule,
#     SolarSchedule, ClockedSchedule
# )
# from django_celery_results.models import TaskResult, GroupResult

#
# admin.site.unregister(User)
# admin.site.unregister(Group)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["id", "type"]
    list_filter = ["type"]


from django.contrib import admin
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

# from django_celery_results.models import TaskResult, GroupResult


# Удаляем модели Celery Beat
# admin.site.unregister(PeriodicTask)
# admin.site.unregister(CrontabSchedule)
# admin.site.unregister(IntervalSchedule)
# admin.site.unregister(SolarSchedule)
# admin.site.unregister(ClockedSchedule)

# # Удаляем модели Celery Result
# admin.site.unregister(TaskResult)
# admin.site.unregister(GroupResult)
