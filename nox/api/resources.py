from django.db import models, IntegrityError
from django.contrib.auth import get_user_model, authenticate
from django.conf.urls import url
from django.core.exceptions import ValidationError
from django import forms
from tastypie.authorization import Authorization
from authorizations import EventAuthorization, PostAuthorization, InviteAuthorization, SubPostAuthorization, OpinionAuthorization
from validations import ModelFormValidation
from tastypie.authentication import Authentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.validation import FormValidation
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.models import ApiKey, create_api_key
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpBadRequest
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest, Unauthorized
from zeropush.models import PushDevice
from zeropush import notify_user, notify_devices
from nox.models import Event, Invite, Post, TextPost, ImagePost, PlacePost, PostComment, PostOpinion
from nox.models import EventForm, CustomUserForm, PostOpinionForm
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
    
    def put_detail(self, request, **kwargs):
        if request.META.get('CONTENT_TYPE').startswith('multipart') and not hasattr(request, '_body'):
            request._body = ''
        return super(MultipartResource, self).put_detail(request, **kwargs)

class CreateUserResource(MultipartResource, ModelResource):
    class Meta:
        queryset = User.objects.all()
        validation = FormValidation(form_class=CustomUserForm)
        resource_name = 'create_user'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['post']
        fields = ['email', 'first_name', 'last_name', 'last_login', 'phone_number', 'icon', 'id']
    
    def obj_create(self, bundle, **kwargs):
        bundle.data['icon_copy'] = bundle.data.get('icon')
        if not bundle.data['icon_copy']:
            bundle.data['icon_copy'] = bundle.obj.get_default_icon()
        bundle.data['icon'] = None;
        bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
        if bundle.data['push_token']:
            device, created = PushDevice.objects.get_or_create(token=bundle.data['push_token'], user=bundle.obj)
        bundle.obj.icon = bundle.data['icon_copy']
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
        
class UserResource(MultipartResource, ModelResource):
    class Meta(CommonMeta):
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'put', 'delete']
        always_return_data = True
        validation = FormValidation(form_class=CustomUserForm)
        fields = ['email', 'first_name', 'last_name', 'last_login', 'phone_number', 'icon', 'id']
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()), 
                                                      self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                                                       self.wrap_view('contact_search'), name="api_contact_search"),
            url(r"^(?P<resource_name>%s)/push_test%s$" % (self._meta.resource_name, trailing_slash()),
                                                          self.wrap_view('push_test'), name="api_push_test"),
            url(r"^(?P<resource_name>%s)/push_token%s$" % (self._meta.resource_name, trailing_slash()),
                                                          self.wrap_view('push_token'), name="api_push_token"),
        ]
    
    def push_token(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        
        token = data.get('push_token')
        if not token:
            return self.create_response(request, 'push_token must be provided.', HttpBadRequest)
        
        device, created = PushDevice.objects.get_or_create(token=token, user=request.user)
        return self.create_response(request, 'push notification token registered with nox.')
        
    def push_test(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        
        alert = data.get('alert', 'nox rox')
        
        notify_user(request.user, alert=alert)
        return self.create_response(request, 'push notification sent')
    
    def contact_search(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
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
        fields = ['id', 'name', 'creator', 'created_at', 'updated_at', 'started_at', 'ended_at', 
                  'latitude', 'longitude', 'venue_id']
        filtering = {
            "id": ALL
        }

class InviteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    event = fields.ForeignKey(EventResource, 'event')
    
    def obj_create(self, bundle, **kwargs):
        bundle = super(InviteResource, self).obj_create(bundle, user=bundle.request.user)
        view = '' if bundle.obj.rsvp else ' view'
        alert = "%s invited you to%s '%s'" % (bundle.request.user.get_full_name(), view, bundle.obj.event.name)
        if bundle.obj.user != bundle.obj.event.creator:
            notify_user(bundle.obj.user, alert=alert)
        return bundle
        
        
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
        bundle = super(TextPostResource, self).obj_create(bundle, user=bundle.request.user)
        # send push notifications
        user_ids = bundle.obj.event.users.filter(~models.Q(id=bundle.request.user.id)).values('id')
        devices = PushDevice.objects.filter(user_id__in=user_ids)
        body = bundle.obj.body
        alert = "%s posted a message to '%s': '" % (bundle.request.user.get_full_name(), bundle.obj.event.name)
        
        if len(alert) + len(body) > 200:
            # Apple allows the push notification payload to be 256 bytes, so 200 is a safe under-estimate
            difference = 200 - len(alert)
            body = body[:difference] + '...'
        alert = alert + body + "'"
        notify_devices(devices, alert=alert)
        return bundle
    
    class Meta(PostMeta):
        queryset = TextPost.objects.all()
        resource_name = 'text_post'

class ImagePostResource(MultipartResource, ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    user = fields.ForeignKey(UserResource, 'user', full=True)
    image = fields.FileField(attribute="image", null=True, blank=True)
    
    def obj_create(self, bundle, **kwargs):
        bundle = super(ImagePostResource, self).obj_create(bundle, user=bundle.request.user)
        #send push notifications
        user_ids = bundle.obj.event.users.filter(~models.Q(id=bundle.request.user.id)).values('id')
        devices = PushDevice.objects.filter(user_id__in=user_ids)
        alert = "%s uploaded a picture to '%s'" % (bundle.request.user.get_full_name(), bundle.obj.event.name)
        notify_devices(devices, alert=alert)
        return bundle
        
    class Meta(PostMeta):
        queryset = ImagePost.objects.all()
        resource_name = 'image_post'

class PlacePostResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    user = fields.ForeignKey(UserResource, 'user', full=True)

    def obj_create(self, bundle, **kwargs):
        bundle = super(PlacePostResource, self).obj_create(bundle, user=bundle.request.user)
        # update the location of the event
        event = bundle.obj.event
        event.latitude = bundle.obj.latitude
        event.longitude = bundle.obj.longitude
        event.venue_id = bundle.obj.venue_id
        event.save()
        # send push notifications
        user_ids = bundle.obj.event.users.filter(~models.Q(id=bundle.request.user.id)).values('id')
        devices = PushDevice.objects.filter(user_id__in=user_ids)
        alert = "%s changed the location of '%s'" % (bundle.request.user.get_full_name(), bundle.obj.event.name)
        notify_devices(devices, alert=alert)
        return bundle

    class Meta(PostMeta):
        queryset = PlacePost.objects.all()
        resource_name = 'place_post'

class PostResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event')
    opinions = fields.ToManyField(UserResource, 'opinions', null=True)
    
    def dehydrate(self, bundle):
        if isinstance(bundle.obj, TextPost):
            text_post_resource = TextPostResource()
            text_post_bundle = text_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = text_post_resource.full_dehydrate(text_post_bundle).data
        elif isinstance(bundle.obj, ImagePost):
            image_post_resource = ImagePostResource()
            image_post_bundle = image_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = image_post_resource.full_dehydrate(image_post_bundle).data
        elif isinstance(bundle.obj, PlacePost):
            place_post_resource = PlacePostResource()
            place_post_bundle = place_post_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = place_post_resource.full_dehydrate(place_post_bundle).data
        bundle.data['comment_count'] = bundle.obj.comments.count()
        bundle.data['like_count'] = bundle.obj.opinions.filter(postopinion=True).count()
        bundle.data['dislike_count'] = bundle.obj.opinions.filter(postopinion=False).count()
        
        try:
            opinion = PostOpinion.objects.get(post=bundle.obj, user=bundle.request.user).opinion
            bundle.data['opinion'] = opinion
        except PostOpinion.DoesNotExist:
            pass
            
        try:
            first_comment = bundle.obj.comments.all()[:1].get()
            post_comment_resource = PostCommentResource()
            post_comment_bundle = post_comment_resource.build_bundle(obj=first_comment, request=bundle.request)
            bundle.data['first_comment'] = post_comment_resource.full_dehydrate(post_comment_bundle).data
        except PostComment.DoesNotExist:
            pass
        return bundle

    class Meta(PostMeta):
        queryset = Post.objects.all().select_subclasses()
        authorization = PostAuthorization()
        resource_name = 'post'
        allowed_methods = ['get']

class PostCommentResource(ModelResource):
    post = fields.ForeignKey(PostResource, 'post')
    user = fields.ForeignKey(UserResource, 'user', full=True)
    fields = ['body', 'post', 'user']
    
    def obj_create(self, bundle, **kwargs):
        bundle = super(PostCommentResource, self).obj_create(bundle, user=bundle.request.user)
        
        return bundle
    
    def build_filters(self, filters=None):
        if 'post__id' not in filters and 'event__id' not in filters:
            raise BadRequest("Comments must be filtered by post or event.")
        return super(PostCommentResource, self).build_filters(filters)
    
    class Meta(CommonMeta):
        queryset = PostComment.objects.all()
        authorization = SubPostAuthorization()
        resource_name = 'post_comment'
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
    
    class Meta(CommonMeta):
        queryset = PostOpinion.objects.all()
        validation = ModelFormValidation(form_class=PostOpinionForm)
        resource_name = 'post_opinion'
        fields = ['id', 'user', 'post', 'opinion']
        authorization = OpinionAuthorization()
        filtering = {
            "post": ALL_WITH_RELATIONS
        }
