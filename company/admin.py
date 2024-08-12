from django.contrib import admin
from django.http import HttpRequest
from leaflet.admin import LeafletGeoAdmin
from company.models import Contacts, ContactUS, PrivacyPolicy, AppInfo, SocialMedia, Sponsor, AboutMistake, ContactWithUsMobile

@admin.register(Contacts)
class ContactsAdmin(LeafletGeoAdmin):
    list_display = ('adress', 'email', 'phone')
    list_display_links = ('adress', 'email', 'phone')
    search_fields = ('adress', 'email', 'phone')

    def has_add_permission(self, request: HttpRequest) -> bool:
        if Contacts.objects.exists():
            return False
        return super().has_add_permission(request)
    

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(ContactUS)
class ContactUSAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone']
    list_display_links = ['id', 'name', 'phone']
    search_fields  = ['id', 'name', 'phone']


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']


    def has_add_permission(self, request: HttpRequest) -> bool:
        if PrivacyPolicy.objects.exists():
            return False
        return super().has_add_permission(request)
    

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False



@admin.register(AppInfo)
class AppInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title']


    def has_add_permission(self, request: HttpRequest) -> bool:
        if AppInfo.objects.all().count() >= 6:
            return False
        return super().has_add_permission(request)
    

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)


    def has_add_permission(self, request: HttpRequest) -> bool:
        if SocialMedia.objects.exists():
            return False
        return super().has_add_permission(request)
    

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)


@admin.register(AboutMistake)
class MistakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'done')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_editable = ('done', )


@admin.register(ContactWithUsMobile)
class ContactWithUSModileAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    list_display_links = ['id', 'email']
    search_fields  = ['id', 'email']