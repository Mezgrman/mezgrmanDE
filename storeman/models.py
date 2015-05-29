from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from mezgrman.utils.classes import ModelFieldIteratorMixin, ModelFieldVerboseNameLookupMixin
from django.db import models
import uuid

class Location(models.Model, ModelFieldIteratorMixin, ModelFieldVerboseNameLookupMixin):
    name = models.CharField(max_length = 100, verbose_name = _("Name"))
    slug = models.SlugField(max_length = 100, blank = True, verbose_name = _("Slug"))
    location = models.CharField(max_length = 100, verbose_name = _("Location"))
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        permissions = (
            ('view_location', "Can view location"),
        )
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('storeman:location-detail', kwargs = {'id': self.pk, 'slug': self.slug})

class Item(models.Model, ModelFieldIteratorMixin, ModelFieldVerboseNameLookupMixin):
    def _filename_generator(instance, filename):
        extension = filename.split(".")[-1]
        return "storeman/itempics/%s.%s" % (uuid.uuid4(), extension.lower())
    
    name = models.CharField(max_length = 100, verbose_name = _("Name"))
    slug = models.SlugField(max_length = 100, blank = True, verbose_name = _("Slug"))
    location = models.ForeignKey(Location, verbose_name = _("Location"))
    amount = models.PositiveIntegerField(default = 1, verbose_name = _("Amount"))
    details = models.TextField(blank = True, verbose_name = _("Details"))
    image = models.ImageField(upload_to = _filename_generator, max_length = 250, blank = True, verbose_name = _("Image"))
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        permissions = (
            ('view_item', "Can view item"),
        )
    
    def __str__(self):
        return _("%(name)s in %(location)s") % {'name': self.name, 'location': self.location.name}
    
    def get_absolute_url(self):
        return reverse('storeman:item-detail', kwargs = {'id': self.pk, 'slug': self.slug})