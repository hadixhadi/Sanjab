from django.contrib import admin
from .models import SimpleStattic
# Register your models here.
@admin.register(SimpleStattic)
class SimpleStaticAdmin(admin.ModelAdmin):
    list_display = ['id','type','date','views']