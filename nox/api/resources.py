from django.db import models, IntegrityError
from django.contrib.auth import get_user_model, authenticate
from django.conf.urls import url
from django.core.exceptions import ValidationError
from django import forms
from tastypie.authorization import Authorization
from authorizations import EventAuthorization, PostAuthorization, InviteAuthorization, SubPostAuthorization
from validations import ModelFormValidation
from tastypie.authentication import Authentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.validation import FormValidation
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.models import ApiKey, create_api_key
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest, Unauthorized
from nox.models import Event, Invite, Post, TextPost, ImagePost, PlacePost, Comment, PostLike, PostDislike
from nox.models import EventForm, CustomUserForm, PostLikeForm, PostDislikeForm
from localflavor.us.forms import USPhoneNumberField
import datetime
import re

User = get_user_model()
# Create API Key for authentication
models.signals.post_save.connect(create_api_key, sender=User)

class CommonMeta:
    authentication = ApiKeyAuthentication()
    authorization = Authorization()
    always_return_data = True

class PostMeta(CommonMeta):
    authorization = PostAuthorization()
    filtering = {
        "event": ALL_WITH_RELATIONS,
        "id": ALL
    }

class PostOpinionMeta(CommonMeta):
    fields = ['id', 'user', 'post']
    authorization = SubPostAuthorization()
    filtering = {
        "post": ALL_WITH_RELATIONS
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
        fields = ['email', 'first_name', 'last_name', 'last_login', 'phone_number']
    
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
        always_return_data = True
        validation = FormValidation(form_class=CustomUserForm)
        fields = ['email', 'first_name', 'last_name', 'last_login', 'phone_number', 'id']
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()), 
                                                      self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                                                       self.wrap_view('contact_search'), name="api_login"),
        ]
    
    def contact_search(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        phone_numbers = set()
        emails = set()
        for contact in data:
            if 'phone_numbers' in contact:
                for phone_number in contact['phone_numbers']:
                    try:
                        phone_number = USPhoneNumberField().clean(re.sub(r"\D", "", phone_number))
                    except ValidationError:
                        continue
                    phone_numbers.add(phone_number)
            if 'emails' in contact:
                for email in contact['emails']:
                    try:
                        email = forms.EmailField().clean(email)
                    except ValidationError:
                        continue
                    emails.add(email)
        users = User.objects.filter(models.Q(phone_number__in=phone_numbers) | models.Q(email__in=emails))
        user_resource = UserResource()
        bundles = [user_resource.build_bundle(obj=user, request=request) for user in users]
        json = [user_resource.full_dehydrate(bundle) for bundle in bundles]
        
        return self.create_response(request, json)
                    

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
                
                user_resource = UserResource()
                user_bundle = user_resource.build_bundle(obj=user, request=request)
                user_json = user_resource.full_dehydrate(user_bundle).data
                return self.create_response(request, {
                    'success': True,
                    'user': user_json,
                    'api_key': api_key.key
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'Your account has been deactivated.',
                }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'Your username or password is incorrect.',
            }, HttpUnauthorized )

class EventResource(ModelResource):
    creator = fields.ForeignKey(UserResource, 'creator')
    
    def obj_create(self, bundle, **kwargs):
        user = bundle.request.user
        if 'started_at' in bundle.data and bundle.data['started_at']:
            started_at = bundle.data['started_at']
        else:
            started_at = datetime.datetime.today()
        bundle = super(EventResource, self).obj_create(bundle, creator=user, started_at=started_at)
        invite = Invite(user=user, event=bundle.obj, rsvp=True)
        invite.save()
        return bundle
    
    class Meta(CommonMeta):
        queryset = Event.objects.all()
        resource_name = 'event'
        always_return_data = True
        authorization = EventAuthorization()
        validation = FormValidation(form_class=EventForm)
        fields = ['id', 'name', 'creator', 'created_at', 'updated_at', 'started_at', 'ended_at']
        filtering = {
            "id": ALL
        }

class InviteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    event = fields.ForeignKey(EventResource, 'event')
    
    class Meta(CommonMeta):
        queryset = Invite.objects.all()
        resource_name = 'invite'
        fields = ['id', 'user', 'event', 'rsvp']
        authorization = InviteAuthorization()
        filtering = {
            "event": ALL_WITH_RELATIONS
        }
        
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
    event = fields.ForeignKey(EventResource, 'event')
    likes = fields.ToManyField(UserResource, 'likes', null=True)
    
    @staticmethod
    def get_opinion(post, user):
        opinion = {
            "dislike": -1,
            "none": 0,
            "like": 1
        }
        if user in post.likes.all():
            return opinion['like']
        elif user in post.dislikes.all():
            return opinion['dislike']
        else:
            return opinion['none']
    
    def dehydrate(self, bundle):
        if isinstance(bundle.obj, TextPost):
            text_post_resource = TextPostResource()
            text_post_bundle = text_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = text_post_resource.full_dehydrate(text_post_bundle).data
        elif isinstance(bundle.obj, ImagePost):
            image_post_resource = ImagePostResource()
            image_post_bundle = image_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = image_post_resource.full_dehydrate(image_post_bundle).data
        bundle.data['comment_count'] = bundle.obj.comment_set.count()
        bundle.data['like_count'] = bundle.obj.likes.count()
        bundle.data['dislike_count'] = bundle.obj.dislikes.count()
        bundle.data['opinion'] = PostResource.get_opinion(bundle.obj, bundle.request.user)
        try:
            first_comment = bundle.obj.comment_set.all()[:1].get()
            post_comment_resource = PostCommentResource()
            post_comment_bundle = post_comment_resource.build_bundle(obj=first_comment, request=bundle.request)
            bundle.data['first_comment'] = post_comment_resource.full_dehydrate(post_comment_bundle).data
        except Comment.DoesNotExist:
            bundle.data['first_comment'] = None;
        return bundle

    class Meta(PostMeta):
        queryset = Post.objects.all().select_subclasses()
        authorization = PostAuthorization()
        resource_name = 'post'

class PostCommentResource(ModelResource):
    post = fields.ForeignKey(PostResource, 'post')
    user = fields.ForeignKey(UserResource, 'user', full=True)
    fields = ['body', 'post', 'user']
    
    def obj_create(self, bundle, **kwargs):
        return super(PostCommentResource, self).obj_create(bundle, user=bundle.request.user)
    
    def build_filters(self, filters=None):
        if 'post__id' not in filters and 'event__id' not in filters:
            raise BadRequest("Comments must be filtered by post or event.")
        return super(PostCommentResource, self).build_filters(filters)
    
    class Meta(CommonMeta):
        queryset = Comment.objects.all()
        authorization = SubPostAuthorization()
        resource_name = 'comment'
        filtering = {
            "post": ALL_WITH_RELATIONS
        }
        
class PostOpinionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    post = fields.ForeignKey(PostResource, 'post')
    
    def obj_create(self, bundle, **kwargs):
        return super(PostOpinionResource, self).obj_create(bundle, user=bundle.request.user)
    
    def build_filters(self, filters=None):
        if 'post__id' not in filters and 'event__id' not in filters:
            raise BadRequest("This resource must be filtered by post or event.")
        return super(PostOpinionResource, self).build_filters(filters)
    
class PostLikeResource(PostOpinionResource):
    class Meta(PostOpinionMeta):
        queryset = PostLike.objects.all()
        validation = ModelFormValidation(form_class=PostLikeForm)
        resource_name = 'post_like'

class PostDislikeResource(ModelResource):
    class Meta(CommonMeta):
        queryset = PostDislike.objects.all()
        validation = ModelFormValidation(form_class=PostDislikeForm)
        resource_name = 'post_dislike'

