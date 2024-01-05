from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id','name','is_done','age']
admin.site.register(Module)
admin.site.register(UserCourse)
admin.site.register(VideoContents)
admin.site.register(CourseInformation)
@admin.register(ModuleSchedule)
class ModuleScheduleAdmin(admin.ModelAdmin):
    list_display = ['user_course','child','module','active_at']
