from django.contrib import admin
from .models import CarToon
# Register your models here.


class CarToonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'item', 'area')
    
admin.site.register(CarToon, CarToonAdmin)    
