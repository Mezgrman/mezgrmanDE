from django.conf.urls import patterns, include, url

urlpatterns = patterns('storeman.views',
    url(r'^items/$', 'items_paged', name = 'items-paged'),
    url(r'^items/page/(?P<page>\d+)/$', 'items_paged', name = 'items-paged'),
    url(r'^locations/$', 'locations_paged', name = 'locations-paged'),
    url(r'^locations/page/(?P<page>\d+)/$', 'locations_paged', name = 'locations-paged'),
    url(r'^items/(?P<id>\d+)-(?P<slug>[a-zA-Z0-9-]+)/$', 'item_detail', name = 'item-detail'),
    url(r'^items/(?P<id>\d+)/edit/$', 'item_edit', name = 'item-edit'),
    url(r'^items/(?P<id>\d+)/delete/$', 'item_delete', name = 'item-delete'),
    url(r'^items/add/$', 'item_create', name = 'item-create'),
    url(r'^locations/(?P<id>\d+)-(?P<slug>[a-zA-Z0-9-]+)/$', 'location_detail', name = 'location-detail'),
    url(r'^locations/(?P<id>\d+)/edit/$', 'location_edit', name = 'location-edit'),
    url(r'^locations/(?P<id>\d+)/delete/$', 'location_delete', name = 'location-delete'),
    url(r'^locations/add/$', 'location_create', name = 'location-create'),
    url(r'^search/$', 'search', name = 'search')
)
