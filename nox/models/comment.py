from django.db import models
from django.conf import settings
from post import Post

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    
    def __unicode__(self):
        return self.body
    
    class Meta:
        db_table = "comment"
        app_label = "nox"
        ordering = ['created_at']