from django.db import models
from django.conf import settings
from post import Post
from django.forms import ModelForm

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    
    class Meta:
        db_table = "post_like"
        app_label = "nox"
        unique_together = ('user', 'post')

class PostLikeForm(ModelForm):
    class Meta:
        model = PostLike
        fields = ['user', 'post']