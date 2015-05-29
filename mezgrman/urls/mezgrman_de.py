from django.conf.urls import patterns, include, url
from django.views.i18n import javascript_catalog
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('mezgrman', ),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^/$', 'mezgrman.views.home', name='home'),
    # url(r'^mezgrman/', include('mezgrman.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^auth/', include('allauth.urls')),
    
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name = 'jsi18n-catalog'),
    url(r'^jsvars/$', 'mezgrman.views.javascript_variables', name = 'jsvars-catalog'),
    url(r"^storeman/", include('storeman.urls', app_name = 'storeman', namespace = 'storeman')),
    url(r"^displays/", include('displays.urls', app_name = 'displays', namespace = 'displays')),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)