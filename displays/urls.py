from django.conf.urls import patterns, include, url

urlpatterns = patterns('displays.views',
    url(r'^$', 'index', name = 'index'),
    url(r'^(?P<id>\d+)/$', 'display', name = 'display'),
    url(r'^(?P<id>\d+)/settings\.json$', 'ajax_settings', name = 'ajax-settings'),
    url(r'^(?P<id>\d+)/bitmap\.json$', 'ajax_bitmap', name = 'ajax-bitmap'),
    url(r'^(?P<id>\d+)/states\.json$', 'ajax_states', name = 'ajax-states'),
    url(r'^(?P<id>\d+)/message\.json$', 'ajax_message', name = 'ajax-message'),
)
