from typing import Iterable
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db import models as gis_models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from common.models import Media
from django.contrib.gis.geos import Point


# Create your models here.
class Contacts(models.Model):
    adress = models.CharField(verbose_name=_('Adress'),max_length=200)
    phone = PhoneNumberField()
    email = models.EmailField(verbose_name=_('Email'))
    latitude = gis_models.FloatField(verbose_name=_('Latitude'))
    longitude = gis_models.FloatField(verbose_name=_('Longitude'))
    location = gis_models.PointField(verbose_name=_('Location'), blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(self.longitude, self.latitude)
        return super().save(*args, **kwargs)

    
    class Meta:
        verbose_name = _('Contacts')
        verbose_name_plural = _('Contacts')


    def __str__(self) -> str:
        return str(self.phone)
    


class ContactUS(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    phone = PhoneNumberField()
    msg = models.TextField(verbose_name=_('Message'))


    class Meta:
        verbose_name = _('Contact US')
        verbose_name_plural = _('Contact US')

    
    def __str__(self) -> str:
        return self.name



class PrivacyPolicy(models.Model):
    text = CKEditor5Field(verbose_name=_('Text'))


    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policy')


    def __str__(self) -> str:
        return str(self.pk)
    


class AppInfo(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'), unique=True)
    description = models.TextField(verbose_name=_('Description'))


    class Meta:
        verbose_name = _('App Info')
        verbose_name_plural = _('App Info')

    
    def __str__(self) -> str:
        return self.title
    

class SocialMedia(models.Model):
    telegram = models.URLField(verbose_name=_('Telegram URL'))
    likedin = models.URLField(verbose_name=_('LinkedIN URL'))
    facebook = models.URLField(verbose_name=_('Facebook URL'))
    instagram = models.URLField(verbose_name=_('Instagram URL'))


    class Meta:
        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Media')

    
    def __str__(self) -> str:
        return f'{str(self.pk)} link'


class Sponsor(models.Model):
    image = models.OneToOneField(to=Media, verbose_name=_('Image'), on_delete=models.CASCADE)
    url = models.URLField(verbose_name=_('URL'))


    class Meta:
        verbose_name = _('Sponsor')
        verbose_name_plural = _('Sponsors')

    
    def __str__(self) -> str:
        return f'{str(self.pk)} sponsor'
    

class AboutMistake(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    done = models.BooleanField(default=False)



    class Meta:
        verbose_name = _('About Mistake')
        verbose_name_plural = _('About Mistakes')

    
    def __str__(self) -> str:
        return self.name
    


class ContactWithUsCategory(models.Model):
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact With Us Category")
        verbose_name_plural = _("Contact With Us Category")


class ContactWithUsReason(models.Model):
    name = models.CharField(_("Name"), max_length=255)
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
    email = models.EmailField(_("Email"))
    message = models.TextField(_("Text"))
    file = models.ForeignKey(Media, verbose_name=_("File"), on_delete=models.CASCADE)
    reason = models.ForeignKey(
        ContactWithUsReason, verbose_name=_("Reason"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Contact With Us Mobile")
        verbose_name_plural = _("Contact With Us Mobile")