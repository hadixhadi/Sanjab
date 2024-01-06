from django.contrib import admin
from .models import *
# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['id','name','type']
    inlines=[
        QuestionInline
    ]


admin.site.register(AnswerQuestion)
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display=['user','exam','grade']