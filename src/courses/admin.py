from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id','name','module','age']
admin.site.register(Module)
@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['id','user','course','child','created_at',
                    'expire_at','is_active','is_graduated']
@admin.register(VideoContents)
class VideoContents(admin.ModelAdmin):
    list_display = ['id','name','url']
admin.site.register(CourseInformation)
@admin.register(ModuleSchedule)
class ModuleScheduleAdmin(admin.ModelAdmin):
    list_display = ['user_course','child','module','active_at']


@admin.register(UserDoneContent)
class UserDoneContentAdmin(admin.ModelAdmin):
    list_display = ['user','content']


@admin.register(CourseSettings)
class CourseSettingsAdmin(admin.ModelAdmin):
    list_display = ['title','expire_day']


@admin.register(ContentPrerequisite)
class ContentPrerequisiteAdmin(admin.ModelAdmin):
    list_display = ['prerequisite_content','content','course']