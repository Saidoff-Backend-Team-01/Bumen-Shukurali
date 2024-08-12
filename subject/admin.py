from django.contrib import admin
from subject.models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']


@admin.register(SubjectTitle)
class SubjectTitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category_name']
    list_display_links = ['id', 'name', 'category_name']
    search_fields = ['name']
    list_filter = ['category__name']


    def category_name(self, obj):
        return obj.category.name
    

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_display_links = ['id', 'name', 'type']
    search_fields = ['name']
    list_filter = ['type']


@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'subject_name']
    list_display_links = ['id', 'user_name', 'subject_name']
    search_fields = ['user__username', 'subject__name']


    def user_name(self, obj):
        return obj.user.username


    def subject_name(self, obj):
        return obj.subject.name


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category_name']
    list_display_links = ['id', 'name', 'category_name']
    search_fields = ['name']
    list_filter = ['category__name']


    def category_name(self, obj):
        return obj.category.name
    

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject_name']
    list_display_links = ['id', 'name', 'subject_name']
    search_fields = ['name']


    def subject_name(self, obj):
        return obj.subject.name
    

@admin.register(ClubMeeting)
class ClubMeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'club_name']
    list_display_links = ['id', 'name', 'club_name']
    search_fields = ['name', 'club__name']
    list_filter = ['club__name']


    def club_name(self, obj):
        return obj.club.name
