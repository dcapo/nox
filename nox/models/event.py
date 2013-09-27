from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.db.models.signals import post_delete
from django.dispatch import receiver
from back_end.settings import USE_S3, MEDIA_ROOT
import shutil

class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_events")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Invite", blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = "event"
        app_label = "nox"
        ordering = ['-started_at']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'creator', 'started_at', 'ended_at']

# Clean up the local event directory.
# This doesn't need to be done in production because S3 uses buckets,
# not directories.
@receiver(post_delete, sender=Event)
def event_delete_handler(sender, **kwargs):
    if not USE_S3:
        event = kwargs['instance']
        dir_to_delete = "%s/event/%d" % (MEDIA_ROOT, event.id)
        shutil.rmtree(dir_to_delete, ignore_errors=True)