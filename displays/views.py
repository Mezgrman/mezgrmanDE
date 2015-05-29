from django.contrib.auth.decorators import user_passes_test
from mezgrman.utils.classes import ExtendedTemplateResponse, JSONResponse
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext_lazy as  _
from django.forms.models import model_to_dict
from pprint import pformat
from .forms import DisplaySettingsForm, TextMessageForm
from .models import DisplaySettings, TextMessage
from annax import MatrixClient
import json

from .settings_secure import *


NAV_DATA = {
    'app_root_view': 'index',
    'app_title': _("Display Manager"),
    'app_navbar_views': [
        (_("Display %s") % 1, ('display', {'id': '1'})),
        (_("Display %s") % 2, ('display', {'id': '2'})),
        (_("Display %s") % 3, ('display', {'id': '3'})),
        (_("Display %s") % 4, ('display', {'id': '4'})),
    ],
}

@permission_required('displays.access_settings', raise_exception = True)
def index(request):
    #client = MatrixClient(SERVER_HOST, SERVER_PORT)
    config = {}#client.get_config(keys = ('power_state', 'stop_indicator'))
    return ExtendedTemplateResponse(request, "displays/index.html", NAV_DATA, {'config': pformat(config)})

@permission_required('displays.access_settings', raise_exception = True)
def display(request, id):
    actual_id = int(id) - 1
    client = MatrixClient(SERVER_HOST, SERVER_PORT)
    config = client.get_config(displays = (actual_id, ))[str(actual_id)]
    message = client.get_message(displays = (actual_id, ))[str(actual_id)]
    settings_form = DisplaySettingsForm(initial = config)
    text_message_form = TextMessageForm()
    
    if not message:
        message_list = []
    else:
        if message['type'] == 'sequence':
            message_list = message['data']
            for index, message in enumerate(message_list):
                # Move the duration field down one level
                message_list[index]['data']['duration'] = message.pop('duration', None)
        else:
            message_list = [message]
    
    _message_list = []
    for message in message_list:
        if message['type'] == 'text':
            name = message['data']['text']
        elif message['type'] == 'bitmap':
            name = "Bitmap name placeholder"
        
        _message_list.append({'name': name, 'json': json.dumps(message)})
    
    return ExtendedTemplateResponse(request, "displays/display.html", NAV_DATA,
        {'config': pformat(config),
        'message_list': enumerate(_message_list),
        'settings_form': settings_form,
        'text_message_form': text_message_form,
        'display_id': id},
        page_title = _("Display %s") % id,
        active_view_include_params = True)

@permission_required('displays.access_settings', raise_exception = True)
def ajax_settings(request, id):
    actual_id = int(id) - 1
    client = MatrixClient(SERVER_HOST, SERVER_PORT)
    
    if request.method == "POST":
        form = DisplaySettingsForm(request.POST)
        if form.is_valid():
            display_settings = form.save(commit = False)
            settings_dict = model_to_dict(display_settings)
            # Strip the 'id' parameter
            settings_dict.pop('id', None)
            status = client.set_config(displays = (actual_id, ), config = settings_dict)
            return JSONResponse(status)
        return JSONResponse({'success': False, 'error': form.errors})
    else:
        config = client.get_config(displays = (actual_id, ))[str(actual_id)]
        return JSONResponse(config)

@permission_required('displays.access_settings', raise_exception = True)
def ajax_bitmap(request, id):
    actual_id = int(id) - 1
    client = MatrixClient(SERVER_HOST, SERVER_PORT)
    
    bitmap = client.get_bitmap(displays = (actual_id, ))[str(actual_id)]
    return JSONResponse(bitmap)

@permission_required('displays.access_settings', raise_exception = True)
def ajax_states(request, id):
    actual_id = int(id) - 1
    client = MatrixClient(SERVER_HOST, SERVER_PORT)
    
    config = client.get_config(displays = (actual_id, ), keys = ('power_state', 'stop_indicator'))[str(actual_id)]
    return JSONResponse(config)

@permission_required('displays.access_settings', raise_exception = True)
def ajax_message(request, id):
    actual_id = int(id) - 1
    client = MatrixClient(SERVER_HOST, SERVER_PORT)
    
    if request.method == "POST":
        if 'message_list' not in request.POST:
            return JSONResponse({'success': False, 'error': "No messages received"})
        
        message_list = json.loads(request.POST.get('message_list'))
        for index, message in enumerate(message_list):
            # Move the duration field up one level
            message_list[index]['duration'] = message['data'].pop('duration', None)
        
        if len(message_list) == 1:
            # No sequence, just a single message
            message = message_list[0]
            message['data'].pop('duration', None)
            _message = client.build_data_message((actual_id, ), message)
            reply = client.send_raw_message(_message)
        else:
            # Build a sequence message
            reply = client.send_sequence_message((actual_id, ), message_list)
        
        return JSONResponse(reply)
    else:
        message = client.get_message(displays = (actual_id, ))[str(actual_id)]
        return JSONResponse(message)