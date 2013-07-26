from django.db import models, IntegrityError
from django.contrib.auth import get_user_model, authenticate
from django.conf.urls import url
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.validation import FormValidation
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.models import ApiKey, create_api_key
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest
from nox.models import Event, Invite, Post, TextPost, ImagePost, PlacePost, Comment
from nox.models import EventForm, CustomUserForm

User = get_user_model()
# Create API Key for authentication
models.signals.post_save.connect(create_api_key, sender=User)

class CommonMeta:
    authentication = BasicAuthentication()
    authorization = Authorization()

class PostMeta(CommonMeta):
    filtering = {
        "event": ALL_WITH_RELATIONS
    }

class CreateUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        validation = FormValidation(form_class=CustomUserForm)
        resource_name = 'create_user'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['post']
        fields = ['email', 'first_name', 'last_name', 'last_login']
    
    def obj_create(self, bundle, **kwargs):
        bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
        bundle.obj.set_password(bundle.data.get('password'))
        bundle.obj.save()
        return bundle
    
    def dehydrate(self, bundle):
        try:
            api_key = ApiKey.objects.get(user=bundle.obj)
        except ApiKey.DoesNotExist:
            raise BadRequest('Failed to retrieve an API Key for the new user.')
        
        bundle.data['api_key'] = api_key.key
        del bundle.data['password']
        return bundle
        
class UserResource(ModelResource):
    class Meta(CommonMeta):
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'put', 'patch', 'delete']
        fields = ['email', 'first_name', 'last_name', 'last_login']
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        
        email = data.get('email', '')
        password = data.get('password', '')
        
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                try:
                    api_key = ApiKey.objects.get(user=user)
                except ApiKey.DoesNotExist:
                    api_key = ApiKey.objects.create(user=user)
                return self.create_response(request, {
                    'success': True,
                    'api_key': api_key.key
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized )

class EventResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        user = bundle.request.user
        bundle = super(EventResource, self).obj_create(bundle)
        invite = Invite(user=user, event=bundle.obj, rsvp=True)
        invite.save()
        return bundle
    
    class Meta(CommonMeta):
        queryset = Event.objects.all()
        resource_name = 'event'
        validation = FormValidation(form_class=EventForm)
        filtering = {
            "id": ALL
        }

class InviteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    event = fields.ForeignKey(EventResource, 'event')
    
    class Meta(CommonMeta):
        queryset = Invite.objects.all()
        resource_name = 'invite'
        fields = ['user', 'event', 'rsvp']
        
class TextPostResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    user = fields.ForeignKey(UserResource, 'user', full=True)
    
    def obj_create(self, bundle, **kwargs):
        return super(TextPostResource, self).obj_create(bundle, user=bundle.request.user)
    
    class Meta(PostMeta):
        queryset = TextPost.objects.all()
        resource_name = 'text_post'

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(MultipartResource, self).deserialize(request, data, format)

class ImagePostResource(MultipartResource, ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    user = fields.ForeignKey(UserResource, 'user', full=True)
    image = fields.FileField(attribute="image", null=True, blank=True)
    
    def obj_create(self, bundle, **kwargs):
        return super(ImagePostResource, self).obj_create(bundle, user=bundle.request.user)
    
    class Meta(PostMeta):
        queryset = ImagePost.objects.all()
        resource_name = 'image_post'

class PlacePostResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    user = fields.ForeignKey(UserResource, 'user', full=True)

    def obj_create(self, bundle, **kwargs):
        return super(TextPostResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta(PostMeta):
        queryset = PlacePost.objects.all()
        resource_name = 'place_post'

class PostResource(ModelResource):
    def dehydrate(self, bundle):
        if isinstance(bundle.obj, TextPost):
            text_post_resource = TextPostResource()
            text_post_bundle = text_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = text_post_resource.full_dehydrate(text_post_bundle).data
        elif isinstance(bundle.obj, ImagePost):
            image_post_resource = ImagePostResource()
            image_post_bundle = image_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = image_post_resource.full_dehydrate(image_post_bundle).data
        return bundle

    class Meta(PostMeta):
        queryset = Post.objects.all().select_subclasses()
        resource_name = 'post'
        filtering = {
            "id": ALL
        }

class PostCommentResource(ModelResource):
    post = fields.ForeignKey(PostResource, 'post')
    user = fields.ForeignKey(UserResource, 'user')
    fields = ['body', 'post', 'user']
    
    def obj_create(self, bundle, **kwargs):
        return super(PostCommentResource, self).obj_create(bundle, user=bundle.request.user)
    
    class Meta(CommonMeta):
        queryset = Comment.objects.all()
        resource_name = 'comment'
        filtering = {
            "post": ALL_WITH_RELATIONS
        }