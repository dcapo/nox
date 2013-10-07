from django.db import models
from post import Post

class PlacePost(Post):
    venue_id = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.venue_id
    
    class Meta:
        db_table = "place_post"
        app_label = "nox"