from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def hello(request):
    return HttpResponse("<img src='https://is1.4sqi.net/userpix/RIT4JWH5ODUAULGA.jpg' />")

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'back_end.views.home', name='home'),
    # url(r'^back_end/', include('back_end.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', hello),
)
