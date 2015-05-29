from mezgrman.utils.classes import ExtendedTemplateResponse
from mezgrman.utils.views import create_model_view, delete_model_view
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext_lazy as  _
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ItemCreationForm, LocationCreationForm
from .models import Item, Location

NAV_DATA = {
    'app_root_view': 'locations-paged',
    'app_title': _("StoreMan"),
    'app_navbar_views': [
        (_("All Items"), 'items-paged'),
        (_("All Locations"), 'locations-paged'),
        (_("Add Item"), 'item-create'),
        (_("Add Location"), 'location-create'),
        (_("Search"), 'search'),
    ],
}

@permission_required('storeman.view_item', raise_exception = True)
def items_paged(request, page = 1):
    qs = Item.objects.all().order_by('-id')
    paginator = Paginator(qs, per_page = 10, orphans = 3)
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    return ExtendedTemplateResponse(request, "storeman/items_paged.html", NAV_DATA, {'items': items},
        page_title = _("All Items"))

@permission_required('storeman.view_location', raise_exception = True)
def locations_paged(request, page = 1):
    qs = Location.objects.all().order_by('-id')
    paginator = Paginator(qs, per_page = 10, orphans = 3)
    
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)
    
    return ExtendedTemplateResponse(request, "storeman/locations_paged.html", NAV_DATA, {'locations': locations},
        page_title = _("All Locations"))

@permission_required('storeman.view_item', raise_exception = True)
def item_detail(request, id, slug):
    item = get_object_or_404(Item, pk = id)
    qs = Item.objects.filter(location = item.location).exclude(id = item.id).order_by('name')
    
    return ExtendedTemplateResponse(request, "storeman/item_detail.html", NAV_DATA, {'item': item},
        page_title = _("Item: %s") % str(item),
        sidebar_title = _("Other Items in %s") % item.location.name,
        sidebar_queryset = qs,
        qs_display_name_func = lambda item: _("%(amount)i× %(name)s") % {'amount': item.amount, 'name': item.name})

@permission_required('storeman.view_location', raise_exception = True)
def location_detail(request, id, slug):
    location = get_object_or_404(Location, pk = id)
    qs = Item.objects.filter(location = location).order_by('name')
    
    return ExtendedTemplateResponse(request, "storeman/location_detail.html", NAV_DATA, {'location': location},
        page_title = _("Location: %s") % str(location),
        sidebar_title = _("Items in %s") % location.name,
        sidebar_queryset = qs,
        qs_display_name_func = lambda item: _("%(amount)i× %(name)s") % {'amount': item.amount, 'name': item.name})

@permission_required('storeman.add_item', raise_exception = True)
def item_create(request):
    return create_model_view(request, ItemCreationForm, 'storeman:locations-paged', NAV_DATA,
        page_title = _("Add Item"),
        form_title = _("Add Item"),
        template = "storeman/item_form.html")

@permission_required('storeman.change_item', raise_exception = True)
def item_edit(request, id):
    item = get_object_or_404(Item, pk = id)
    return create_model_view(request, ItemCreationForm, ('storeman:item-detail', {'id': item.pk, 'slug': item.slug}), NAV_DATA,
        page_title = _("Edit Item: %s") % str(item),
        form_title = _("Edit Item"),
        instance = item,
        template = "storeman/item_form.html")

@permission_required('storeman.delete_item', raise_exception = True)
def item_delete(request, id):
    item = get_object_or_404(Item, pk = id)
    return delete_model_view(request, item, 'storeman:locations-paged', ('storeman:item-detail', {'id': item.pk, 'slug': item.slug}), NAV_DATA,
        page_title = _("Delete Item: %s") % str(item),
        template = "storeman/item_delete.html")

@permission_required('storeman.add_location', raise_exception = True)
def location_create(request):
    return create_model_view(request, LocationCreationForm, 'storeman:locations-paged', NAV_DATA,
        page_title = _("Add Location"),
        form_title = _("Add Location"),
        template = "storeman/location_form.html")

@permission_required('storeman.edit_location', raise_exception = True)
def location_edit(request, id):
    location = get_object_or_404(Location, pk = id)
    return create_model_view(request, LocationCreationForm, ('storeman:location-detail', {'id': location.pk, 'slug': location.slug}), NAV_DATA,
        page_title = _("Edit Location: %s") % str(location),
        form_title = _("Edit Location"),
        instance = location,
        template = "storeman/location_form.html")

@permission_required('storeman.delete_location', raise_exception = True)
def location_delete(request, id):
    location = get_object_or_404(Location, pk = id)
    return delete_model_view(request, location, 'storeman:locations-paged', ('storeman:location-detail', {'id': location.pk, 'slug': location.slug}), NAV_DATA,
        page_title = _("Delete Location: %s") % str(location),
        template = "storeman/location_delete.html")

@permission_required('storeman.view_item', raise_exception = True)
def search(request):
    data = {}
    if request.method == "POST":
        query = request.POST.get('query').strip()
        if query:
            data['query'] = query
            data['results'] = Item.objects.filter(Q(name__icontains = query) | Q(details__icontains = query)).order_by('name')
    return ExtendedTemplateResponse(request, "storeman/search.html", NAV_DATA, data,
        page_title = _("Search"))