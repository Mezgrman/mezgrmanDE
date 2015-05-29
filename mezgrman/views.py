from django.http import HttpResponse
from django.conf import settings

import json

def javascript_variables(request):
    variables = {
        'STATIC_PREFIX': settings.STATIC_URL
    }
    
    var_catalog = "// VARIABLE CATALOG FOR DJANGO VARIABLES\n\n"
    var_catalog += "\n".join(("%s = %s;" % (key, json.dumps(value)) for key, value in variables.items()))
    return HttpResponse(var_catalog, content_type = 'text/javascript')