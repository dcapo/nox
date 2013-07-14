from django.db import models
from django.conf import settings
from event import Event

class Invite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.ForeignKey(Event)
    rsvp = models.BooleanField()
    
    class Meta:
        db_table = "invite"
        app_label = "nox"