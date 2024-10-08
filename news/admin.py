from django.contrib import admin

from news.models import News,NewsImage

# Register your models here.

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ["id", "news", "image"]


class NewsImageInline(admin.StackedInline):
    model = NewsImage
    extra = 1
    show_change_link = True

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    inlines = [NewsImageInline]