from django.core.urlresolvers import resolve, reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .functions import view_tuple

import json

class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503

class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504

class ExtendedTemplateResponse(TemplateResponse):
    """
    A TemplateResponse with support for navigation and sidebar entries.
    """
    
    def __init__(self, request, template, nav_data = {}, context = None, page_title = None, sidebar_title = None, sidebar_queryset = None, qs_display_name_func = lambda item: item, active_view_include_params = False, nav_data_resolve_views = True, content_type = None, status = None, current_app = None):
        if context is None:
            context = {}
        
        # Only look up the URLs once, then save the result in the nav_data
        if nav_data and nav_data_resolve_views and (nav_data.get('app_root') is None or nav_data.get('app_navbar') is None):
            current_view_data = resolve(request.path)
            namespace = current_view_data.namespaces[0]
            
            app_root_view = view_tuple(nav_data.get('app_root_view', ""))
            nav_data['app_root'] = reverse(":".join((namespace, app_root_view[0])),
                args = app_root_view[1],
                kwargs = app_root_view[2])
            
            if nav_data.get('app_navbar') is None:
                nav_data['app_navbar'] = []
                for title, view_name in nav_data.get('app_navbar_views', []):
                    view = view_tuple(view_name)
                    active = False # This will be done later
                    nav_data['app_navbar'].append((
                        title,
                        reverse(":".join((namespace, view[0])), args = view[1], kwargs = view[2]),
                        active))
        
        if nav_data:
            # Re-set the active page indicator every time
            if nav_data_resolve_views:
                app_navbar_views = nav_data.get('app_navbar_views', [])
                if app_navbar_views:
                    current_view_data = resolve(request.path)
                    for index, entry in enumerate(app_navbar_views):
                        title, view_name = entry
                        view = view_tuple(view_name)
                        if active_view_include_params:
                            active = current_view_data.url_name == view[0] and current_view_data.args == view[1] and current_view_data.kwargs == view[2]
                        else:
                            active = current_view_data.url_name == view[0]
                        nav_data['app_navbar'][index] = (
                            nav_data['app_navbar'][index][0],
                            nav_data['app_navbar'][index][1],
                            active)
            else:
                app_navbar = nav_data.get('app_navbar', [])
                if app_navbar:
                    for index, entry in enumerate(app_navbar):
                        name, path = entry
                        active = path == request.path
                        nav_data['app_navbar'][index] = (
                            nav_data['app_navbar'][index][0],
                            nav_data['app_navbar'][index][1],
                            active)
            
            context.update(nav_data)
        
        # Add page title
        context['page_title'] = page_title
        
        # Add sidebar data
        context['sidebar_title'] = sidebar_title
        context['sidebar_queryset'] = ((item, qs_display_name_func(item)) for item in sidebar_queryset) if sidebar_queryset else None
        return super().__init__(request, template, context, content_type, status, current_app)

class JSONResponse(HttpResponse):
    """
    A response with JSON encoded data for use in APIs.
    """
    
    def __init__(self, content = {}, content_type = 'application/json', status = 200, reason = None, charset = None):
        json_content = json.dumps(content)
        return super().__init__(json_content, content_type, status, reason, charset)

class ModelFieldIteratorMixin(object):
    """
    A mixin implementing iteration
    """
    
    def iter_fields(self, exclude = []):
        for field in (f for f in self._meta.fields if f.name not in exclude):
            yield (field.verbose_name, getattr(self, field.name))

class ModelFieldVerboseNameLookupMixin(object):
    """
    A mixin implementing verbose field name lookup
    """
    
    def get_verbose_field_name(self, field_name):
        return self._meta.get_field(field_name).verbose_name