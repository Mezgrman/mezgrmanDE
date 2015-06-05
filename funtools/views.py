from mezgrman.utils.classes import ExtendedTemplateResponse
from django.utils.translation import ugettext_lazy as  _
from mezgrman.utils.functions import multiline_join
from .text_converter_charmaps import *

import random

NAV_DATA = {
    'app_root_view': 'index',
    'app_title': _("Fun Tools"),
    'app_navbar_views': [
        (_("Text Converters"), 'text-converters'),
    ],
}

def index(request):
    return ExtendedTemplateResponse(request, "funtools/index.html", NAV_DATA,
        page_title = _("Index"))

def text_converters(request):
    def _convert_text(text, charmap, separator = ""):
        text = text.strip()
        result_chars = [charmap.get(char, char) for char in text]
        result = multiline_join(result_chars, separator)
        return result

    def _mess_up(text, amount = 1.0):
        MODIFIERS = (
            # Going up
            '\u030d', '\u030e', '\u0304', '\u0305',
            '\u033f', '\u0311', '\u0306', '\u0310',
            '\u0352', '\u0357', '\u0351', '\u0307',
            '\u0308', '\u030a', '\u0342', '\u0343',
            '\u0344', '\u034a', '\u034b', '\u034c',
            '\u0303', '\u0302', '\u030c', '\u0350',
            '\u0300', '\u0301', '\u030b', '\u030f',
            '\u0312', '\u0313', '\u0314', '\u033d',
            '\u0309', '\u0363', '\u0364', '\u0365',
            '\u0366', '\u0367', '\u0368', '\u0369',
            '\u036a', '\u036b', '\u036c', '\u036d',
            '\u036e', '\u036f', '\u033e', '\u035b',
            '\u0346', '\u031a',
            
            # Going down
            '\u0316', '\u0317', '\u0318', '\u0319',
            '\u031c', '\u031d', '\u031e', '\u031f',
            '\u0320', '\u0324', '\u0325', '\u0326',
            '\u0329', '\u032a', '\u032b', '\u032c',
            '\u032d', '\u032e', '\u032f', '\u0330',
            '\u0331', '\u0332', '\u0333', '\u0339',
            '\u033a', '\u033b', '\u033c', '\u0345',
            '\u0347', '\u0348', '\u0349', '\u034d',
            '\u034e', '\u0353', '\u0354', '\u0355',
            '\u0356', '\u0359', '\u035a', '\u0323',
            
            # Staying in the middle
            '\u0315', '\u031b', '\u0340', '\u0341',
            '\u0358', '\u0321', '\u0322', '\u0327',
            '\u0328', '\u0334', '\u0335', '\u0336',
            '\u034f', '\u035c', '\u035d', '\u035e',
            '\u035f', '\u0360', '\u0362', '\u0338',
            '\u0337', '\u0361', '\u0489',
        )
        
        if amount >= 1.0:
            result = "".join([char + "".join([random.choice(MODIFIERS) for i in range(int(amount))]) for char in text])
        else:
            result = "".join([text[x] + random.choice(MODIFIERS) if divmod(x, (1 / amount))[1] == 0.0 else text[x] for x in range(len(text))])
        return result
    
    template_vars = {}
    
    if request.method == "POST" and 'text' in request.POST and 'type' in request.POST:
        t = request.POST.get('type')
        text = request.POST.get('text')
        template_vars['text'] = text
        
        if t == 'big':
            result = _convert_text(text.upper(), CHARMAP_BIG, separator = "  ")
        elif t == 'flip':
            result = _convert_text(text[::-1], CHARMAP_FLIP)
        elif t == 'elegant':
            result = _convert_text(text, CHARMAP_ELEGANT)
        elif t == 'elegant-bold':
            result = _convert_text(text, CHARMAP_ELEGANT_BOLD)
        elif t == 'gothic':
            result = _convert_text(text, CHARMAP_GOTHIC)
        elif t == 'gothic-bold':
            result = _convert_text(text, CHARMAP_GOTHIC_BOLD)
        elif t == 'sans':
            result = _convert_text(text, CHARMAP_SANS)
        elif t == 'sans-bold':
            result = _convert_text(text, CHARMAP_SANS_BOLD)
        elif t == 'sans-italic':
            result = _convert_text(text, CHARMAP_SANS_ITALIC)
        elif t == 'sans-italic-bold':
            result = _convert_text(text, CHARMAP_SANS_ITALIC_BOLD)
        elif t == 'mono':
            result = _convert_text(text, CHARMAP_MONO)
        elif t == 'serif-bold':
            result = _convert_text(text, CHARMAP_SERIF_BOLD)
        elif t == 'serif-italic':
            result = _convert_text(text, CHARMAP_SERIF_ITALIC)
        elif t == 'serif-italic-bold':
            result = _convert_text(text, CHARMAP_SERIF_ITALIC_BOLD)
        elif t == 'doublestruck':
            result = _convert_text(text, CHARMAP_DOUBLESTRUCK)
        elif t == 'fullwidth':
            result = _convert_text(text, CHARMAP_FULLWIDTH)
        elif t == 'messed-up-low':
            result = _mess_up(text, amount = 1.0)
        elif t == 'messed-up-medium':
            result = _mess_up(text, amount = 5.0)
        elif t == 'messed-up-high':
            result = _mess_up(text, amount = 10.0)
        elif t == 'messed-up-insane':
            result = _mess_up(text, amount = 100.0)
        elif t == 'strikethrough-horizontal':
            result = "".join(["\u0336" + c for c in text])
        elif t == 'strikethrough-diagonal':
            result = "".join(["\u0338" + c for c in text])
        
        template_vars['result'] = result
    
    return ExtendedTemplateResponse(request, "funtools/text_converters.html", NAV_DATA, template_vars,
        page_title = _("Text Converters"))
