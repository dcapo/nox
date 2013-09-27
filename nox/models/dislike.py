from django.db import models
from django.conf import settings
from post import Post
from django.forms import ModelForm

class PostDislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    
    class Meta:
        db_table = "post_dislike"
        app_label = "nox"
        unique_together = ('user', 'post')

class PostDislikeForm(ModelForm):
    class Meta:
        model = PostDislike
        fields = ['user', 'post']