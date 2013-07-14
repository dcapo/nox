from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from tastypie.api import Api
from nox.api import EventResource, UserResource, InviteResource, TextPostResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EventResource())
v1_api.register(InviteResource())
v1_api.register(TextPostResource())

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
