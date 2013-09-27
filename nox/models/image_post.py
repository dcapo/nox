from django.db import models
from post import Post
import os
import string
import random
from back_end.settings import USE_S3
from storages.backends.s3boto import S3BotoStorage
from django.db.models.signals import post_delete
from django.dispatch import receiver

class ImagePost(Post):
    def random_filename(self, size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    
    def get_upload_location(instance, filename):
        extension = os.path.splitext(filename)[-1]
        print(extension)
        prefix = instance.random_filename()
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
    path = image_post.image.path
    if path:
        storage.delete(path)