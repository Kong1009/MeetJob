from django.contrib import admin
from .models import Movies
# Register your models here.

class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    
admin.site.register(Movies, MoviesAdmin)
