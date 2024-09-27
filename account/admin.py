from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Groups, User, UserMessage, UserOtpCode


class UserMessageInlineAdmin(admin.StackedInline):
    model = UserMessage
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = [UserMessageInlineAdmin]
    list_display = ("id", "phone_number", "email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "birth_date", "photo")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        # (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)

admin.site.register(Groups)


class UserMessageAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(UserMessage, UserMessageAdmin)


@admin.register(UserOtpCode)
class UserOtpCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "code", "type")
