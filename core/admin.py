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
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'event', 
        'read_at', 
        'created_at',
    ]
@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'event_type', 
        'channel', 
        'enabled',
    ]
@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = [
        'notification',
        'channel', 
        'status', 
        'sent_at',
        'retry_count',
        'failure_reason', 
    ]
    
