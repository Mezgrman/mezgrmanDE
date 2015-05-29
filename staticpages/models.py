from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

LANG_CHOICES = (
    ('en', _("English")),
    ('de', _("German"))
)

TEMPLATE_CHOICES = (
    ('default', _("Default")),
    ('minimal', _("Minimal")),
)

class StaticPageGroup(models.Model):
    # Identification criteria
    site = models.ForeignKey(Site, blank = True, null = True, verbose_name = _("Site"))
    subdomain_regex = models.CharField(max_length = 100, verbose_name = _("Subdomain RegEx"))
    base_path_regex = models.CharField(max_length = 100, verbose_name = _("Base Path RegEx"))
    
    # Other attributes
    nav_data = models.TextField(blank = True, verbose_name = _("Navigation Data"),
        help_text = _("In YAML format"))
    
    def __str__(self):
        return "%s.%s/%s" % (self.subdomain_regex, self.site.domain or "*", self.base_path_regex.lstrip("/"))

class StaticPage(models.Model):
    # Identification criteria
    site = models.ForeignKey(Site, blank = True, null = True, verbose_name = _("Site"))
    subdomain_regex = models.CharField(max_length = 100, blank = True, verbose_name = _("Subdomain RegEx"))
    path_regex = models.CharField(max_length = 100, verbose_name = _("Path RegEx"),
        help_text = _("Make sure to match the end of the string when using a page group! (use $)"))
    lang = models.CharField(max_length = 100, choices = LANG_CHOICES, verbose_name = _("Language"))
    rank = models.PositiveIntegerField(default = 0, verbose_name = _("Page Rank"),
        help_text = _("If multiple pages are available for a request, the highest ranked page will be served."))
    
    # Other attributes
    group = models.ForeignKey(StaticPageGroup, blank = True, null = True, verbose_name = _("Page Group"))
    copy_of = models.ForeignKey('StaticPage', blank = True, null = True, verbose_name = _("Copy of"))
    page_title = models.CharField(max_length = 100, blank = True, verbose_name = _("Page Title"))
    template = models.CharField(max_length = 100, choices = TEMPLATE_CHOICES, blank = True, verbose_name = _("Template"))
    parse = models.BooleanField(verbose_name = _("Parse Template Tags"))
    mimetype = models.CharField(max_length = 25, blank = True, verbose_name = _("MIME Type"))
    redirect_url = models.URLField(max_length = 500, blank = True, verbose_name = _("Redirect URL"))
    redirect_permanent = models.BooleanField(verbose_name = _("Permanent Redirect"))
    head_extras = models.TextField(blank = True, verbose_name = _("Extra HTML Head Code"))
    variables = models.TextField(blank = True, verbose_name = _("Template Variables"),
        help_text = _("In YAML format"))
    content = models.TextField(blank = True, verbose_name = _("Content"))
    
    def __str__(self):
        if self.group:
            return "[%s] (%s)/%s" % (self.lang, self.group, self.path_regex.lstrip("/"))
        else:
            return "[%s] %s.%s/%s" % (self.lang, self.subdomain_regex, self.site.domain if self.site else "*", self.path_regex.lstrip("/"))