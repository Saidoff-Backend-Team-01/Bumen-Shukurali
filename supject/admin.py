from django.contrib import admin

from .models import (
    Category,
    Club,
    ClubMeeting,
    Step,
    StepFile,
    StepTest,
    Subject,
    SubjectTitle,
    TestAnswer,
    TestQuestion,
    UserStep,
    UserSubject,
    UserTestResult,
    UserTotalTestResult,
    Vacancy,
)

admin.site.register(TestQuestion)
admin.site.register(TestAnswer)
admin.site.register(UserTotalTestResult)
admin.site.register(Club)
admin.site.register(ClubMeeting)


class SubjectTitleInline(admin.StackedInline):
    model = SubjectTitle
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "click_count")
    inlines = [SubjectTitleInline]


class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 1
    show_change_link = True


@admin.register(SubjectTitle)
class SubjectTitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = [SubjectInline]


class StepInlineAdmin(admin.StackedInline):
    model = Step
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    inlines = [StepInlineAdmin]


@admin.register(UserSubject)
class UserSubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(StepFile)
class StepFileAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class StepFileInlineAdmin(admin.StackedInline):
    model = StepFile
    extra = 1


@admin.register(UserStep)
class UserStepAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(StepTest)
class StepTestAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    inlines = [StepFileInlineAdmin]
