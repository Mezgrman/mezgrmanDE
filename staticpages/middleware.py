from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from mezgrman.utils.classes import ExtendedTemplateResponse
from django.template import RequestContext, Template
from .models import StaticPage, StaticPageGroup
from django.conf import settings
from django.db.models import Q

import re
import yaml

class StaticPagesMiddleware(object):
    """
    This middleware adds support for database-managed, static pages.
    """
    
    def process_response(self, request, response):
        if response.status_code != 404:
            # Only look for static pages when no view could be found
            return response
        
        try:
            try:
                # First look for standalone pages only (no group members)
                # Only get pages for the current site or universal pages (with no site specified)
                potential_pages = StaticPage.objects.filter(Q(group = None) & (Q(site = request.site) | Q(site = None)))
                if not potential_pages: raise ValueError
                
                # Filter out pages with no matching path
                potential_pages = [page for page in potential_pages if re.match(page.path_regex, request.path)]
                if not potential_pages: raise ValueError
                
                # Filter out pages with no matching subdomain
                potential_pages = [page for page in potential_pages if re.match(page.subdomain_regex, request.subdomain or "")]
                if not potential_pages: raise ValueError
            except ValueError:
                # Look for groups for the current site or universal groups (with no site specified)
                potential_groups = StaticPageGroup.objects.filter(Q(site = request.site) | Q(site = None))
                if not potential_groups: raise ValueError
                
                # Filter out groups with no matching base path
                potential_groups = [group for group in potential_groups if re.match(group.base_path_regex, request.path)]
                if not potential_groups: raise ValueError
                
                # Filter out groups with no matching subdomain
                potential_groups = [group for group in potential_groups if re.match(group.subdomain_regex, request.subdomain or "")]
                if not potential_groups: raise ValueError
                
                # Get all pages in the potential groups
                potential_pages = StaticPage.objects.filter(group__in = potential_groups)
                if not potential_pages: raise ValueError
                
                # Get all pages with matching path
                potential_pages = [page for page in potential_pages if re.search(page.path_regex, request.path)]
                if not potential_pages: raise ValueError
        except ValueError:
            # No page found, just return the original response
            return response
        
        # We have at least one potential page, now filter by language
        lang_matching_pages = [page for page in potential_pages if page.lang == request.LANGUAGE_CODE]
        if not lang_matching_pages:
            # No page found in the desired language, fall back to the default language
            lang_matching_pages = [page for page in potential_pages if page.lang == settings.LANGUAGE_CODE]
            if not lang_matching_pages:
                # Still no page found, so just use what's available
                lang_matching_pages = potential_pages
        
        # Now just take the highest ranked page out of the remaining candidates
        page = sorted(lang_matching_pages, key = lambda p: p.rank, reverse = True)[0]
        
        # Okay, we have our page. Now serve it
        
        if page.copy_of:
            # We have a copied page
            page = page.copy_of
        
        if page.redirect_url:
            # We have a redirect
            if page.redirect_permanent:
                return HttpResponsePermanentRedirect(page.redirect_url)
            else:
                return HttpResponseRedirect(page.redirect_url)
        
        if not page.template:
            # Return a bare HttpResponse
            return HttpResponse(page.content, content_type = page.mimetype)
        
        if page.parse:
            page.content = Template(page.content).render(RequestContext(request))
        
        variables = yaml.load(page.variables) if page.variables else {}
        variables.update({'page': page})
        return ExtendedTemplateResponse(request, "staticpages/%s.html" % page.template,
            nav_data = yaml.load(page.group.nav_data) if page.group else None,
            context = variables,
            page_title = page.page_title,
            nav_data_resolve_views = False).render()