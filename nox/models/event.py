from django.conf import settings
from django.db import models
from django.forms import ModelForm

class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    ended_at = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255)
    asset_dir = models.CharField(max_length=64)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Invite", blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = "event"
        app_label = "nox"

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'asset_dir', 'ended_at']