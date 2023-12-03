from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Type)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(AnswerQuestion)
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display=['user','exam','grade']