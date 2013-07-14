from django.db import models
from post import Post

class PlacePost(Post):
    name = models.CharField(max_length=255)
    venue_id = models.PositiveIntegerField()
    
    class Meta:
        db_table = "place_post"
        app_label = "nox"