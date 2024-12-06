from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Media
from supject.models import UserTotalTestResult

from .managers import CustomUserManager


class User(AbstractUser):
    class AuthType(models.TextChoices):
        GOOGLE = "GOOGLE", _("Google Account")
        FACEBOOK = "FACEBOOK", _("Facebook Account")
        TELEGRAM = "TELEGRAM", _("Telegram Account")
        WITH_EMAIL = "WITH EMAIL", _("Email Auth")
        WITH_PHONE = "WITH PHONE", _("Phone Auth")

    class GenderType(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    username = models.CharField(max_length=123, null=True, blank=True)
    birth_date = models.DateField(_("birth_date"), null=True, blank=True)
    photo = models.ForeignKey(
        Media, on_delete=models.SET_NULL, null=True, blank=True, related_name="photo"
    )
    email = models.EmailField(_("email address"), null=True, blank=True)
    phone_number = models.CharField(
        _("phone number"), max_length=20, null=True, blank=True
    )
    father_name = models.CharField(
        _("father name"), max_length=120, null=True, blank=True
    )
    auth_type = models.CharField(
        _("auth type"),
        choices=AuthType.choices,
        max_length=244,
        default=AuthType.WITH_PHONE,
    )
    gender = models.CharField(
        _("gender"), choices=GenderType.choices, null=True, blank=True
    )
    telegram_id = models.CharField(
        _("telegram id"), max_length=55, null=True, blank=True
    )
    objects = CustomUserManager()
    device_id = models.CharField(_("device id"), max_length=244, null=True, blank=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        if self.phone_number:
            return f"{self.phone_number}"
        return f"{self.email}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @property
    def user_total_bal(self):
        filtered_user_results = UserTotalTestResult.objects.filter(user=self)
        total_bal = (
            filtered_user_results.aggregate(total_ball=Sum("ball"))["total_ball"]
            / filtered_user_results.count()
        )

        return total_bal


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

    def add_member(self, user):
        if not self.users.filter(id=user.id).exists():
            self.users.add(user)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

class UserGroupConversation(models.Model):
    initiator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user_group_conversatons_started"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user_group_conversatons_receiver"
    )
    start_time = models.DateTimeField(auto_now_add=True)

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

    conversation = models.ForeignKey(UserGroupConversation, on_delete=models.CASCADE, related_name="user_messages", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    views = models.ManyToManyField(verbose_name=_('Views'), to='UserView')
    likes = models.ManyToManyField(verbose_name=_('Likes'), to='UserLike')


    def __str__(self) -> str:
        return f"{self.user.username} - {self.group.name}"

    class Meta:
        verbose_name = _("User's message")
        verbose_name_plural = _("User's messages")


class SocialUser(models.Model):
    class RegisterType(models.TextChoices):
        GOOGLE = "GOOGLE", _("google")
        FACEBOOK = "FACEBOOK", _("facebook")
        TELEGRAM = "TELEGRAM", _("telegram")

    user = models.ForeignKey(
        verbose_name=_("User"), to=User, on_delete=models.CASCADE, null=True, blank=True
    )
    social_user_id = models.IntegerField(_("user id"), null=True, blank=True)
    provider = models.CharField(
        _("provider"), choices=RegisterType.choices, max_length=255
    )
    email = models.EmailField(_("email address"), unique=True)
    extra_data = models.JSONField(_("extra data"), default=dict)


class IntroQuestion(models.Model):
    title = models.CharField(verbose_name=_("Introduction question"), max_length=200)
    more_info = models.TextField(verbose_name=_("More info"))

    def __str__(self) -> str:
        return self.title


class IntroQuestionAnswer(models.Model):
    text = models.TextField(verbose_name=_("Answer"))
    intro_question = models.ForeignKey(
        verbose_name=_("Question"),
        to=IntroQuestion,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    def __str__(self) -> str:
        return self.text


class UserIntroQuestion(models.Model):
    user = models.ForeignKey(verbose_name=_("User"), to=User, on_delete=models.CASCADE)
    intro_question = models.ForeignKey(
        verbose_name=_("Question"),
        to=IntroQuestion,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    answer = models.ManyToManyField(
        verbose_name=_("Answer"),
        to=IntroQuestionAnswer,
        related_name= 'answers'
    )
    is_marked = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.intro_question.title}"


class UserView(models.Model):
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)


    def __str__(self):
        return f'{self.user.pk} - {self.created_at}'
    

class UserLike(models.Model):
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)


    def __str__(self):
        return f'{self.user.pk} - {self.created_at}'