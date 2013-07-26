from django.db import models
from django.conf import settings
from post import Post

class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    
    def __unicode__(self):
        return self.body
    
    class Meta:
        db_table = "comment"
        app_label = "nox"