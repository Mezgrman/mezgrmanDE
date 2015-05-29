class SiteVariablesMiddleware(object):
    """
    Set site-specific variables
    """
    
    def process_request(self, request):
        setattr(request, 'site_navbar_filename', "sitenav/%s.html" % request.site.domain)
        return None