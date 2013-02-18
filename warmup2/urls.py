from django.conf.urls import patterns, include, url
from warmup2.views import *
from warmup2 import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmup2.views.home', name='home'),
    # url(r'^warmup2/', include('warmup2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	(r'^$', client),
	(r'^(?P<path>.*(js|css|jpg|png|ico))$', 'django.views.static.serve', {'document_root':settings.PROJECT_DIR + '/media/'}),
	(r'^users/.*$', userLogin),
	(r'^TESTAPI/.*$', testAPI),
)
