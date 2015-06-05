from django.conf.urls import patterns, include, url

urlpatterns = patterns('funtools.views',
    url(r'^$', 'index', name = 'index'),
    url(r'^textconverters/$', 'text_converters', name = 'text-converters'),
)
