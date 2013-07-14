from django.db import models
from post import Post

class ImagePost(Post):
    def get_upload_location(instance, filename):
        return "images/%s/%s" % (instance.event_id, instance.id)

    image = models.ImageField(upload_to=get_upload_location)
    
    class Meta:
        db_table = "image_post"
        app_label = "nox"