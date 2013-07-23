from django.db import models
from post import Post
import os
import string
import random

class ImagePost(Post):
    def random_filename(self, size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    
    def get_upload_location(instance, filename):
        extension = os.path.splitext(filename)[-1]
        print(extension)
        prefix = instance.random_filename()
        filename = "%s%s" % (prefix, extension)
        return "event/%s/%s" % (instance.event_id, filename)

    image = models.ImageField(upload_to=get_upload_location)
    
    def __unicode__(self):
        return self.image
    
    class Meta:
        db_table = "image_post"
        app_label = "nox"