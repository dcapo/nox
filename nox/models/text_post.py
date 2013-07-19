from django.db import models
from post import Post

class TextPost(Post):
    body = models.TextField()
    
    def __unicode__(self):
        return self.body
    
    class Meta:
        db_table = "text_post"
        app_label = "nox"