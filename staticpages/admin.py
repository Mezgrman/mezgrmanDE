from django.contrib import admin
from .models import StaticPage, StaticPageGroup

admin.site.register(StaticPage)
admin.site.register(StaticPageGroup)