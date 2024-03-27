from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ExamDone)
class ExamDoneAdmin(admin.ModelAdmin):
    list_display=['user','child','exam','created_at']


class QuestionInline(admin.TabularInline):
    model = Question
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['id','name','type']
    inlines=[
        QuestionInline
    ]

@admin.register(AnswerQuestion)
class AnswerQuestionAdmin(admin.ModelAdmin):
    list_display = ['id','user','child','exam','question','answer']
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display=['user','child','exam','grade']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id","question","type","exam"]