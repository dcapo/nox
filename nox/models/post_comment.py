from django.db import models
from django.conf import settings
from post import Post

class PostComment(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    
    def __unicode__(self):
        return self.body
    
    class Meta:
        db_table = "post_comment"
        app_label = "nox"
        ordering = ['created_at']