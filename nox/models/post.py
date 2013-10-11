from django.db import models
from django.conf import settings

from event import Event
from model_utils.managers import InheritanceManager

class Post(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    event = models.ForeignKey(Event)
    opinions = models.ManyToManyField(settings.AUTH_USER_MODEL, through="PostOpinion", blank=True, related_name="opinions")
    
    objects = InheritanceManager()
    
    class Meta:
        db_table = "post"
        app_label = "nox"
        ordering = ['-created_at']