from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import Media
from django.utils.translation import gettext_lazy as _
from common.models import Media
from account.managers import UserManager


# Create your models here.
class User(AbstractUser):
    class AuthType(models.TextChoices):
        GOOGLE = "GOOGLE", _("Google Account")
        FACEBOOK = "FACEBOOK", _("Facebook Account")
        TELEGRAM = "TELEGRAM", _("Telegram Account")
        WITH_EMAIL = "WITH EMAIL", _("Email Account")
    
    username = models.CharField(max_length=200, blank=True, null=True)
    auth_type = models.CharField(_("auth type"), choices=AuthType.choices)
    photo = models.OneToOneField(verbose_name=_('Photo'), to=Media, null=True, blank=True, on_delete=models.SET_NULL)
    birthday = models.DateTimeField(verbose_name=_('Birthday Data'), auto_now=True, blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()


    def __str__(self) -> str:
        return self.username
    

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    

class Groups(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    users = models.ManyToManyField(verbose_name=_('Users'), to=User, related_name='groupusers')

    def __str__(self) -> str:
        return self.name
    

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
    

class UserMessage(models.Model):
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_('Message'))
    file = models.OneToOneField(verbose_name=_('File'), to=Media, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(verbose_name=_('Group'), to=Groups, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.user.username} - {self.group.name}"
    

    class Meta:
        verbose_name = _('User\'s message')
        verbose_name_plural = _('User\'s messages')
    

