from django.contrib import admin
from common.models import Media, FAQ, Advertising
# Register your models here.


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    list_display_links = ['id', 'type']
    search_fields = ['id']
    list_filter = ['type']
    


admin.site.register(FAQ)
admin.site.register(Advertising)


from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask, CrontabSchedule, IntervalSchedule,
    SolarSchedule, ClockedSchedule
)
from django_celery_results.models import TaskResult, GroupResult


# Удаляем модели Celery Beat
admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)

# Удаляем модели Celery Result
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
