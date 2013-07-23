from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from tastypie.api import Api
from nox.api import EventResource, UserResource, InviteResource, PostResource, TextPostResource, ImagePostResource, PlacePostResource
from . import settings

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EventResource())
v1_api.register(InviteResource())
v1_api.register(TextPostResource())
v1_api.register(ImagePostResource())
v1_api.register(PlacePostResource())
v1_api.register(PostResource())

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    (r'^(?P<path>.*)$', 'django.views.static.serve', 
       {'document_root': settings.MEDIA_ROOT}),
)