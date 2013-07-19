from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.validation import FormValidation
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from nox.models import Event, Invite, TextPost
from nox.models import EventForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['email', 'first_name', 'last_name', 'last_login']

class EventResource(ModelResource):
    text_posts = fields.ToManyField('nox.api.TextPostResource', 'textpost_set', null=True, blank=True, full=True)
    # users = fields.ToManyField('nox.api.UserResource', 'users')
    
    def obj_create(self, bundle, **kwargs):
        user = bundle.request.user
        bundle = super(EventResource, self).obj_create(bundle)
        invite = Invite(user=user, event=bundle.obj, rsvp=True)
        invite.save()
        return bundle
    
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        authentication = BasicAuthentication()
        authorization = Authorization()
        validation = FormValidation(form_class=EventForm)
        filtering = {
            "id": ALL
        }

class InviteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    event = fields.ForeignKey(EventResource, 'event')
    
    class Meta:
        queryset = Invite.objects.all()
        resource_name = 'invite'
        fields = ['user', 'event', 'rsvp']
        
class TextPostResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    user = fields.ForeignKey(UserResource, 'user', full=True)
    
    def obj_create(self, bundle, **kwargs):
        return super(TextPostResource, self).obj_create(bundle, user=bundle.request.user)
    
    class Meta:
        queryset = TextPost.objects.all()
        resource_name = 'text_post'
        authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            "event": ALL_WITH_RELATIONS
        }