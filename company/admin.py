from django.contrib import admin

from .models import FAQ, Contacts, ContactWithUs, SocialMedia

# Register your models here.


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number"]
    list_editable = ["phone_number"]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["id", "telegram"]
    list_display_links = ["id", "telegram"]


@admin.register(ContactWithUs)
class ContactWithUsAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "message"]
    search_fields = ["phone_number"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "answer"]
