import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Name"),
                ),
                (
                    "click_count",
                    models.PositiveIntegerField(default=0, verbose_name="Click Count"),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categorys",
            },
        ),
        migrations.CreateModel(
            name="Step",

            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Title")),
                ("order", models.PositiveIntegerField(verbose_name="Order")),
                ("description", models.TextField(verbose_name="Description")),
            ],
            options={
                "verbose_name": "Step",
                "verbose_name_plural": "Steps",
            },
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Name")),
                (
                    "type",
                    models.CharField(
                        choices=[("local", "Local"), ("global", "Global")],
                        max_length=50,
                        verbose_name="Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Subject",
                "verbose_name_plural": "Subjects",
            },
        ),
        migrations.CreateModel(
            name="Club",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Title")),
                ("order", models.PositiveIntegerField(verbose_name="Order")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="clubusers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users",
                    ),
                ),
                (
                    "subject",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.subject",
                        verbose_name="Subject",
                    ),
                ),
            ],
            options={
                "verbose_name": "Step",
                "verbose_name_plural": "Steps",
            },
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Name")),
                (
                    "type",
                    models.CharField(
                        choices=[("local", "Local"), ("global", "Global")],
                        max_length=50,
                        verbose_name="Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Subject",
                "verbose_name_plural": "Subjects",
            },
        ),
        migrations.CreateModel(
            name="Club",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="Club 1", max_length=100, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default="initial club", verbose_name="Description"
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="clubusers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users",
                    ),
                ),
                (
                    "subject",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.subject",
                        verbose_name="Subject",
                    ),
                ),
            ],
            options={
                "verbose_name": "Club",
                "verbose_name_plural": "Clubs",
            },
        ),
        migrations.CreateModel(
            name="ClubMeeting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("location", models.URLField(verbose_name="Location link")),
                ("date", models.DateTimeField(auto_now=True)),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.club",
                        verbose_name="Club",
                    ),
                ),
            ],
            options={
                "verbose_name": "Club Meeting",
                "verbose_name_plural": "Club Meetings",
            },
        ),
        migrations.CreateModel(
            name="StepFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="title")),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.media",
                        verbose_name="File",
                    ),
                ),
                (
                    "step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="step_files",
                        to="supject.step",
                        verbose_name="Step",
                    ),
                ),
            ],
            options={
                "verbose_name": "Step's file",
                "verbose_name_plural": "Step's files",
            },
        ),
        migrations.CreateModel(
            name="StepTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ball_for_each_test",
                    models.FloatField(verbose_name="Bal for each question"),
                ),
                (
                    "question_count",
                    models.PositiveIntegerField(verbose_name="Question Count"),
                ),
                (
                    "test_type",
                    models.CharField(
                        choices=[("midterm", "Midterm"), ("final", "Final")],
                        max_length=30,
                        verbose_name="Test type",
                    ),
                ),
                ("time_for_test", models.DurationField(verbose_name="Test time limit")),
                (
                    "step",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tests",
                        to="supject.step",
                        verbose_name="Step",
                    ),
                ),
            ],
            options={
                "verbose_name": "Step's test",
                "verbose_name_plural": "Step's tests",
            },
        ),
        migrations.AddField(
            model_name="step",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="steps",
                to="supject.subject",
                verbose_name="Subject",
            ),
        ),
        migrations.CreateModel(
            name="SubjectTitle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Name")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.category",
                        verbose_name="Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Subject title",
                "verbose_name_plural": "Subject titles",
            },
        ),
        migrations.AddField(
            model_name="subject",
            name="subject_title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subjects",
                to="supject.subjecttitle",
                verbose_name="Subject title",
            ),
        ),
        migrations.CreateModel(
            name="TestQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question_type",
                    models.CharField(
                        choices=[("multiple", "Multiple"), ("single", "Single")],
                        max_length=30,
                        verbose_name="Question type",
                    ),
                ),
                (
                    "question",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="question"),
                ),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("easy", "easy"),
                            ("medium", "medium"),
                            ("hard", "hard"),
                        ],
                        default="easy",
                        max_length=10,
                    ),
                ),
                (
                    "steptest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_questions",
                        to="supject.steptest",
                        verbose_name="Step test",
                    ),
                ),
            ],
            options={
                "verbose_name": "Test's question",
                "verbose_name_plural": "Test's questions",
            },
        ),
        migrations.CreateModel(
            name="TestAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer", models.TextField(verbose_name="Answer")),
                ("is_correct", models.BooleanField(verbose_name="Is correct")),
                (
                    "test_quetion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_answers",
                        to="supject.testquestion",
                        verbose_name="Question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Test's answer",
                "verbose_name_plural": "Test's answers",
            },
        ),
        migrations.CreateModel(
            name="UserTestResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("test_answers", models.ManyToManyField(to="supject.testanswer")),
                (
                    "test_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.testquestion",
                        verbose_name="Question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users",
                    ),
                ),
            ],
            options={
                "verbose_name": "Test result",
                "verbose_name_plural": "Test results",
            },
        ),
        migrations.CreateModel(
            name="UserTotalTestResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ball", models.FloatField(blank=True, null=True, verbose_name="Bal")),
                (
                    "correct_answers",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Count of correct answers"
                    ),
                ),
                ("finished", models.BooleanField(default=False)),
                ("percentage", models.IntegerField(blank=True, null=True)),
                (
                    "step_test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.steptest",
                        verbose_name="Step test",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users",
                    ),
                ),
                (
                    "user_test_results",
                    models.ManyToManyField(
                        related_name="testresults",
                        to="supject.usertestresult",
                        verbose_name="Test Results",
                    ),
                ),
            ],
            options={
                "verbose_name": "Total test result",
                "verbose_name_plural": "Total test results",
            },
        ),
        migrations.AddField(
            model_name="usertestresult",
            name="total_result",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="total_results",
                to="supject.usertotaltestresult",
            ),
        ),
        migrations.CreateModel(
            name="Vacancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supject.category",
                        verbose_name="Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vacancy",
                "verbose_name_plural": "Vacancies",
            },
        ),
        migrations.CreateModel(
            name="UserStep",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("finished", models.BooleanField(default=False)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                (
                    "step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_steps",
                        to="supject.step",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_steps",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "step")},
            },
        ),
        migrations.CreateModel(
            name="UserSubject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_test_ball",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Total test ball"
                    ),
                ),
                ("started_time", models.DateTimeField(auto_now_add=True)),
                ("started", models.BooleanField(default=False)),
                ("finished", models.BooleanField(default=False)),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_subjects",
                        to="supject.subject",
                        verbose_name="Subject",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User's subject",
                "verbose_name_plural": "User's subjects",
                "unique_together": {("user", "subject")},
            },
        ),
    ]
