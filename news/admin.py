from django.contrib import admin

from news.models import News,NewsImage

# Register your models here.


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ["id", "news", "image"]
