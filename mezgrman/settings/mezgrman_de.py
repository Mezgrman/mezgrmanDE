from .base import *

SITE_ID = 1
ROOT_URLCONF = 'mezgrman.urls.mezgrman_de'

SUBDOMAIN_URLCONFS = {
    
}

ALLOWED_HOSTS += [
	".mezgrman.de",
]

INSTALLED_APPS += [
    'storeman',
    'displays',
]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mezgrman.wsgi.mezgrman_de.application'