from django.db import models
from post import Post
import os
from back_end.settings import USE_S3
from storages.backends.s3boto import S3BotoStorage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from nox.util import Util

class ImagePost(Post):
    def get_upload_location(instance, filename):
        extension = os.path.splitext(filename)[-1]
        prefix = Util.random_filename()
        filename = "%s%s" % (prefix, extension)
        return "event/%s/%s" % (instance.event_id, filename)
    
    storage = S3BotoStorage() if USE_S3 else None
    image = models.ImageField(storage=storage, upload_to=get_upload_location)
    
    def __unicode__(self):
        return self.image.name
    
    class Meta:
        db_table = "image_post"
        app_label = "nox"

@receiver(post_delete, sender=ImagePost)
def image_post_delete_handler(sender, **kwargs):
    image_post = kwargs['instance']
    storage = image_post.image.storage
    image_url = image_post.image.url
    storage.delete(image_post.image.url)