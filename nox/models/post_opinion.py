from django.db import models
from django.conf import settings
from post import Post
from django.forms import ModelForm

class PostOpinion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    opinion = models.BooleanField()
    
    class Meta:
        db_table = "post_opinion"
        app_label = "nox"
        unique_together = ('user', 'post')

class PostOpinionForm(ModelForm):
    class Meta:
        model = PostOpinion
        fields = ['user', 'post', 'opinion']