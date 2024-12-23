from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


from common.models import Media


# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, unique=True)
    click_count = models.PositiveIntegerField(verbose_name=_("Click Count"), default=0)
    bg_image = models.OneToOneField(
        verbose_name=_("Image"),
        to=Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="image",
    )
    icon = models.OneToOneField(
        verbose_name=_("Icon"),
        to=Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="icon",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")


class Subject(models.Model):
    class SubjectType(models.TextChoices):
        LOCAL = "local", _("Local")
        GLOBAL = "global", _("Global")

    name = models.CharField(verbose_name=_("Name"), max_length=200)
    category = models.ForeignKey(  # O'zgartirilgan
        verbose_name=_("Category"),
        to=Category,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    image = models.OneToOneField(
        Media, on_delete=models.CASCADE, related_name="subjects", null=True, blank=True
    )

    def clean(self):
        subject_count = Subject.objects.filter(category=self.category).count()
        if subject_count >= 2:
            raise ValidationError(_("Invalid Subject Type"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")


class UserSubject(models.Model):
    subject = models.ForeignKey(
        verbose_name=_("Subject"),
        to=Subject,
        on_delete=models.CASCADE,
        related_name="user_subjects",
    )
    user = models.ForeignKey(
        verbose_name=_("User"), to="account.User", on_delete=models.CASCADE
    )
    total_test_ball = models.PositiveIntegerField(
        verbose_name=_("Total test ball"), default=0
    )
    started_time = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.subject.name}"

    class Meta:
        verbose_name = _("User's subject")
        verbose_name_plural = _("User's subjects")
        unique_together = ("user", "subject")


class Vacancy(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    category = models.ForeignKey(
        verbose_name=_("Category"), to=Category, on_delete=models.CASCADE
    )
    description = models.TextField(verbose_name=_("Description"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancies")


class Club(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, default="Club 1")
    subject = models.OneToOneField(
        verbose_name=_("Subject"), to=Subject, on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        verbose_name=_("Users"), to="account.User", related_name="clubusers", blank=True
    )
    description = models.TextField(
        verbose_name=_("Description"), default="initial club"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Club")
        verbose_name_plural = _("Clubs")


class ClubMeeting(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    location = models.URLField(verbose_name=_("Location link"))
    date = models.DateTimeField(auto_now=True)
    club = models.ForeignKey(verbose_name=_("Club"), to=Club, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Club Meeting")
        verbose_name_plural = _("Club Meetings")


class Step(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    order = models.PositiveIntegerField(verbose_name=_("Order"))
    subject = models.ForeignKey(
        verbose_name=_("Subject"),
        to=Subject,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    description = CKEditor5Field(_("Description"))

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Step")
        verbose_name_plural = _("Steps")


class StepFile(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=250)
    file = models.ForeignKey(verbose_name=_("File"), to=Media, on_delete=models.CASCADE)
    step = models.ForeignKey(
        verbose_name=_("Step"),
        to=Step,
        on_delete=models.CASCADE,
        related_name="step_files",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Step's file")
        verbose_name_plural = _("Step's files")


class StepTest(models.Model):

    class TestTypes(models.TextChoices):
        MIDTERM = "midterm"
        FINAL = "final"

    step = models.OneToOneField(
        verbose_name=_("Step"), to=Step, on_delete=models.CASCADE, related_name="tests"
    )
    ball_for_each_test = models.FloatField(verbose_name=_("Bal for each question"))
    question_count = models.PositiveIntegerField(verbose_name=_("Question Count"))
    test_type = models.CharField(
        verbose_name=_("Test type"), max_length=30, choices=TestTypes.choices
    )
    time_for_test = models.DurationField(verbose_name=_("Test time limit"))

    def __str__(self) -> str:
        return f"{self.pk} - {self.step.title}"

    class Meta:
        verbose_name = _("Step's test")
        verbose_name_plural = _("Step's tests")


class TestQuestion(models.Model):
    class QuestionLevel(models.TextChoices):
        EASY = "easy", _("easy")
        MEDIUM = "medium", _("medium")
        HARD = "hard", _("hard")

    class QuestionType(models.TextChoices):
        MULTIPLE = "multiple", _("Multiple")
        SINGLE = "single", _("Single")
        ORDERING = "ordering", _("Ordering")

    steptest = models.ForeignKey(
        verbose_name=_("Step test"),
        to=StepTest,
        on_delete=models.CASCADE,
        related_name="test_questions",
    )
    question_type = models.CharField(
        verbose_name=_("Question type"), max_length=30, choices=QuestionType.choices
    )
    question = CKEditor5Field(_("question"), config_name="extends")
    level = models.CharField(
        max_length=10, choices=QuestionLevel.choices, default=QuestionLevel.EASY
    )

    def __str__(self) -> str:
        return f"{self.pk}"

    class Meta:
        verbose_name = _("Test's question")
        verbose_name_plural = _("Test's questions")


class TestAnswer(models.Model):
    test_quetion = models.ForeignKey(
        verbose_name=_("Question"),
        to=TestQuestion,
        on_delete=models.CASCADE,
        related_name="test_answers",
    )
    answer = CKEditor5Field(_("question"), config_name="extends")
    is_correct = models.BooleanField(verbose_name=_("Is correct"))
    order = models.PositiveIntegerField(_("order"), null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.is_correct}"

    class Meta:
        verbose_name = _("Test's answer")
        verbose_name_plural = _("Test's answers")


class UserTestResult(models.Model):
    total_result = models.ForeignKey(
        "UserTotalTestResult", on_delete=models.CASCADE, related_name="total_results"
    )
    test_question = models.ForeignKey(
        verbose_name=_("Question"), to=TestQuestion, on_delete=models.CASCADE
    )
    test_answers = models.ManyToManyField(TestAnswer)
    user = models.ForeignKey(
        verbose_name=_("Users"), to="account.User", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.pk} - {self.user.username}"

    class Meta:
        verbose_name = _("Test result")
        verbose_name_plural = _("Test results")


class UserTotalTestResult(models.Model):
    step_test = models.ForeignKey(
        verbose_name=_("Step test"), to=StepTest, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=_("Users"), to="account.User", on_delete=models.CASCADE
    )
    ball = models.FloatField(verbose_name=_("Bal"), null=True, blank=True)
    correct_answers = models.PositiveIntegerField(
        verbose_name=_("Count of correct answers"), null=True, blank=True
    )
    user_test_results = models.ManyToManyField(
        verbose_name=_("Test Results"), to=UserTestResult, related_name="testresults"
    )
    finished = models.BooleanField(default=False)
    percentage = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.user.username}"

    class Meta:
        verbose_name = _("Total test result")
        verbose_name_plural = _("Total test results")


class UserStep(models.Model):
    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="user_steps"
    )
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="user_steps")
    finished = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "step"]


class UserClubMessage(models.Model):
    user = models.ForeignKey(verbose_name=_("User"), to="account.User", on_delete=models.CASCADE, related_name='club_messages')
    message = models.TextField(verbose_name=_("Message"))
    file = models.OneToOneField(
        verbose_name=_("File"),
        to=Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    club = models.ForeignKey(
        verbose_name=_("Club"), to=Club, on_delete=models.CASCADE, related_name='club_messages'
    )
    views = models.ManyToManyField(verbose_name=_('Views'), to='account.UserView')
    created_at = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    

    def __str__(self) -> str:
        return f"{self.user.pk} - {self.club.name}"

    class Meta:
        verbose_name = _("Club's message")
        verbose_name_plural = _("Club's messages")
