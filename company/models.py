from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from phonenumber_field.modelfields import PhoneNumberField

from account.models import User
from common.models import Media

from .validators import (
    phone_number_validator,
    validate_instagram_url,
    validate_telegram_url,
)


# Create your models here.
class Contacts(models.Model):
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, validators=[phone_number_validator])
    email = models.EmailField()
    location = models.URLField()

    class Meta:
        verbose_name = "Contacts"


class SocialMedia(models.Model):
    telegram = models.URLField(validators=[validate_telegram_url])
    facebook = models.URLField(validators=[])
    instagram = models.URLField(validators=[validate_instagram_url])
    linkedin = models.URLField(validators=[])

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Medias"


class ContactWithUs(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    message = models.TextField()

    class Meta:
        verbose_name = _("Contact With Us")
        verbose_name_plural = _("Contact With Us")


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = "FAQ"


class PrivacyPolicy(models.Model):
    text = CKEditor5Field(_("text"))

    class Meta:
        verbose_name = _("Privacy Policy")
        verbose_name_plural = _("Privacy Policy")

    def __str__(self) -> str:
        return str(self.pk)


class AppInfo(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"), unique=True)
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("App Info")
        verbose_name_plural = _("App Info")

    def __str__(self) -> str:
        return self.title


class Sponsor(models.Model):
    image = models.OneToOneField(
        to=Media, verbose_name=_("Image"), on_delete=models.CASCADE
    )
    url = models.URLField(verbose_name=_("URL"))

    class Meta:
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __str__(self) -> str:
        return f"{str(self.pk)} sponsor"


class AboutMistake(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    done = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("About Mistake")
        verbose_name_plural = _("About Mistakes")

    def __str__(self) -> str:
        return self.name


class ContactWithUsCategory(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact With Us Category")
        verbose_name_plural = _("Contact With Us Category")


class ContactWithUsReason(models.Model):
    name = models.CharField(_("name"), max_length=255)
    category = models.ForeignKey(
        ContactWithUsCategory,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name="contact_with_us_reasons",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact With Us Reason")
        verbose_name_plural = _("Contact With Us Reason")


class ContactWithUsMobile(models.Model):
    email = models.EmailField(_("email"))
    message = models.TextField(_("text"))
    file = models.ForeignKey(Media, verbose_name=_("File"), on_delete=models.CASCADE)
    reason = models.ForeignKey(
        ContactWithUsReason, verbose_name=_("Reason"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Contact With Us Mobile")
        verbose_name_plural = _("Contact With Us Mobile")


class Notification(models.Model):
    title = models.CharField(_("title"), max_length=50)
    message = models.TextField(_("message"))
    is_all_users = models.BooleanField(_("is_all_users"), default=False)
    users = models.ManyToManyField(User)
    extra_data = models.JSONField(_("extra data"))
    scheduled_date = models.DateTimeField(_("scheduled date"), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
