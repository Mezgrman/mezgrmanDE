from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .classes import ExtendedTemplateResponse
from .functions import view_tuple

def create_model_view(request, form_class, abort_view, nav_data, page_title, form_title, instance = None, template = "generic_form.html"):
    """
    A generic view for adding or editing a model instance using a form.
    """
    
    if request.method == "POST":
        if 'save' in request.POST:
            form = form_class(request.POST, request.FILES, instance = instance)
            if form.is_valid():
                instance = form.save()
                return HttpResponseRedirect(instance.get_absolute_url())
            return ExtendedTemplateResponse(request, template, nav_data, {'form': form})
        else:
            view_name, args, kwargs = view_tuple(abort_view)
            return HttpResponseRedirect(reverse(view_name, args = args, kwargs = kwargs))
    
    form = form_class(instance = instance)
    return ExtendedTemplateResponse(request, template, nav_data, {'form': form, 'form_title': form_title},
        page_title = page_title)

def delete_model_view(request, instance, success_view, abort_view, nav_data, page_title, template = "generic_delete.html"):
    """
    A generic view for deleting a model instance using a form.
    """
    
    if request.method == "POST":
        if 'confirm' in request.POST:
            instance.delete()
            view_name, args, kwargs = view_tuple(success_view)
        else:
            view_name, args, kwargs = view_tuple(abort_view)
        
        return HttpResponseRedirect(reverse(view_name, args = args, kwargs = kwargs))
    
    return ExtendedTemplateResponse(request, template, nav_data, {'instance': instance},
        page_title = page_title)

def model_detail_view(request, instance, nav_data, page_title, exclude_fields = ['id'], template = "generic_detail.html"):
    """
    A generic view for viewing details of a model instance.
    """
    
    fields = instance.iter_fields(exclude = exclude_fields)
    
    return ExtendedTemplateResponse(request, template, nav_data, {'instance': instance, 'fields': fields},
        page_title = page_title)