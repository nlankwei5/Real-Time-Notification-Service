from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display =[
        'actor', 
        'source',
        'event_type', 
        'object_type',
        'object_id',
        'created_at',
    ]