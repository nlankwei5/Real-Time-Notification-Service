from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  
# Create your models here.

EVENT_TYPE = (
    ("FOLLOW", "Follow"),
    ("LIKE", "Like"),
    ("PAYMENT", "Payment"),
    ("COMMENT", "Comment"),
    ("ACCIDENT", "Accident"),
    ("CONGESTION", "Congestion"),
    ("MALFUNCTION", "Malfunction"),


)

CHANNELS = [
        ("in_app", "In App"),
        ("email", "Email"),
        ("push", "Push Notification"),
    ]
class Event(models.Model):

    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE)
    object_type = models.CharField(max_length=50)
    object_id = models.IntegerField()
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor or self.source}  performed {self.event_type}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name="notifications")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        if self.read_at:
            return
        self.read_at = timezone.now()
        self.save()
        

    def __str__(self):
        return f"Notification for {self.user}"
    


class NotificationPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_preferences")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE)
    channel = models.CharField(max_length=20, choices=CHANNELS)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "event_type", "channel")

    def __str__(self):
        return f"{self.user} - {self.event_type} ({self.channel})"
    

class NotificationDelivery(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="deliveries")
    channel = models.CharField(max_length=20, choices=CHANNELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    retry_count= models.IntegerField(default=0, )
    failure_reason = models.TextField(null=True, blank=True)