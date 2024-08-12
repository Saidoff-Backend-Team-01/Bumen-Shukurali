from django.contrib import admin
from news.models import News, NewsImage, NewsView
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(NewsView)
class NewsViewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip']
    list_display_links = ['id', 'ip']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title']
    filter_horizontal = ['views']


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']
    


admin.site.unregister(Group)