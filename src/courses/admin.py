from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Module)
admin.site.register(UserCourse)
@admin.register(ModuleSchedule)
class ModuleScheduleAdmin(admin.ModelAdmin):
    list_display = ['user_course','child','module','active_at']
