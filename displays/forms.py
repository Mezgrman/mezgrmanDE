from django import forms
from django.utils.translation import ugettext_lazy as  _
from .models import DisplaySettings, TextMessage

class DisplaySettingsForm(forms.ModelForm):
    class Meta:
        model = DisplaySettings
        fields = '__all__'
    
    power_state = forms.BooleanField(required = False, initial = False, label = _("Enable Matrix"))
    stop_indicator = forms.BooleanField(required = False, initial = False, label = _("Enable Stop Indicator"))
    display_mode = forms.ChoiceField(label = _("Display Mode"), choices = (
        ('auto', _("Automatic")),
        ('static', _("Static")),
        ('scroll', _("Scrolling"))
    ))
    scroll_direction = forms.ChoiceField(label = _("Scroll Direction"), choices = (
        ('left', _("Left")),
        ('right', _("Right"))
    ))
    scroll_mode = forms.ChoiceField(label = _("Scroll Mode"), choices = (
        ('repeat-on-disappearance', _("Repeat after Disappearance")),
        ('repeat-on-end', _("Repeat instantly")),
        ('repeat-after-gap', _("Repeat with space"))
    ))
    scroll_speed = forms.IntegerField(label = _("Scroll Speed"), min_value = 1, max_value = 25, initial = 1)
    scroll_step = forms.IntegerField(label = _("Scroll Step"), min_value = 1, max_value = 5, initial = 1)
    scroll_gap = forms.IntegerField(label = _("Scroll Gap"), min_value = 0, max_value = 15, initial = 5)
    blink_frequency = forms.IntegerField(label = _("Blink Speed"), min_value = 0, max_value = 100, initial = 0)
    stop_indicator_blink_frequency = forms.IntegerField(label = _("Stop Indicator Blink Speed"), min_value = 0, max_value = 100, initial = 0)

class TextMessageForm(forms.ModelForm):
    class Meta:
        model = TextMessage
        fields = '__all__'
    
    text = forms.CharField(label = _("Text"))
    align = forms.ChoiceField(label = _("Align"), choices = (
        ('', "-" * 10),
        ('center', _("Center")),
        ('left', _("Left")),
        ('right', _("Right"))
    ))
    font = forms.ChoiceField(label = _("Font"), choices = (
        ('pixelmix', "PixelMix (8px)"),
        ('press start 2p', "Press Start 2P (8px)"),
        ('nokia cellphone fc', "Nokia Cellphone FC (8px)"),
        ('metoopixzi', "Me Too Pixzi (6px)"),
        ('graph 35+ pix', "Graph 35+ Pix (8px)"),
        ('fipps', "Fipps (8px)"),
        ('minecraftia', "Minecraftia (8px)")
    ))
    size = forms.IntegerField(label = _("Font Size"), min_value = 1, max_value = 20, initial = 8)
    parse_time_string = forms.BooleanField(label = _("Parse Time String"))
    blend_bitmap = forms.BooleanField(label = _("Blend Bitmap"))
    use_config = forms.BooleanField(label = _("Specific Configuration"))
    duration = forms.FloatField(label = _("Display Duration"), min_value = 0.1, max_value = 3600.0, initial = 5.0)