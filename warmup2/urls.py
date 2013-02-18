from django.conf.urls import patterns, include, url
from warmup1.views import *
from warmup1 import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmup1.views.home', name='home'),
    # url(r'^warmup1/', include('warmup1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	(r'^$', client),
	(r'^(?P<path>.*js)$', 'django.views.static.serve', {'document_root':settings.PROJECT_DIR + '/media/'}),
	(r'^(?P<path>.*css)$', 'django.views.static.serve', {'document_root':settings.PROJECT_DIR + '/media/'}),
	(r'^users/.*$', userLogin),
	(r'^TESTAPI/.*$', testAPI),
)
