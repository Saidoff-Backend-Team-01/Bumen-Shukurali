from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Media

from .managers import CustomUserManager


class User(AbstractUser):
    class AuthType(models.TextChoices):
        GOOGLE = "GOOGLE", _("Google Account")
        FACEBOOK = "FACEBOOK", _("Facebook Account")
        TELEGRAM = "TELEGRAM", _("Telegram Account")
        WITH_EMAIL = "WITH EMAIL", _("Email Account")

    birth_date = models.DateField(_("birth_date"), null=True, blank=True)
    photo = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    auth_type = models.CharField(_("auth type"), choices=AuthType.choices, max_length=244)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_token(self):
        return RefreshToken.access_token


class UserOtpCode(models.Model):
    class VerificationType(models.TextChoices):
        REGISTER = "register"
        RESET_PASSWORD = "reset_password"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    type = models.CharField(_("type"), max_length=20, choices=VerificationType.choices)
    expires_in = models.DateTimeField(_("expires_in"), null=True, blank=True)
    is_used = models.BooleanField(_("is_used"), default=False)

    def __str__(self) -> str:
        return self.code


class Groups(models.Model):
    name = models.CharField(_("name"), max_length=100)
    users = models.ManyToManyField(User, related_name="user_groups")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class UserMessage(models.Model):
    user = models.ForeignKey(verbose_name=_("User"), to=User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_("Message"))
    file = models.OneToOneField(
        verbose_name=_("File"),
        to=Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        verbose_name=_("Group"), to=Groups, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.user.username} - {self.group.name}"

    class Meta:
        verbose_name = _("User's message")
        verbose_name_plural = _("User's messages")


class SocialUser(models.Model):
    class RegisterType(models.TextChoices):
        GOOGLE = "google", _("google")
        FACEBOOK = "facebook", _("facebook")
        TELEGRAM = "telegram", _("telegram")

    user = models.ForeignKey(
        verbose_name=_("User"), to=User, on_delete=models.CASCADE, null=True, blank=True
    )
    social_user_id = models.IntegerField(_("user id"), null=True, blank=True)
    provider = models.CharField(_("provider"), choices=RegisterType.choices, max_length=255, default=RegisterType.GOOGLE)
    email = models.EmailField(_("email address"), unique=True)
    extra_data = models.JSONField(_("extra data"), default=dict)
