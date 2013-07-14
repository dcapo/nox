from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from geoposition.fields import GeopositionField

from inheritance_cast_model import InheritanceCastModel
from event import Event

class Post(InheritanceCastModel):
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    event = models.ForeignKey(Event)
    
    def __unicode__(self):
        return str(self.real_type)
    
    class Meta:
        abstract = True