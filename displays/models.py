from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class DisplaySettings(models.Model):
    class Meta:
        permissions = (
            ('access_settings', "Can access Display Settings"),
        )
    
    power_state = models.BooleanField()
    stop_indicator = models.BooleanField()
    display_mode = models.CharField(max_length = 100)
    scroll_direction = models.CharField(max_length = 100)
    scroll_mode = models.CharField(max_length = 100)
    scroll_speed = models.PositiveIntegerField()
    scroll_step = models.PositiveIntegerField()
    scroll_gap = models.PositiveIntegerField()
    blink_frequency = models.PositiveIntegerField()
    stop_indicator_blink_frequency = models.PositiveIntegerField()

class TextMessage(models.Model):
    text = models.CharField(max_length = 1000)
    align = models.CharField(max_length = 100)
    font = models.CharField(max_length = 100)
    size = models.PositiveIntegerField()
    parse_time_string = models.BooleanField()
    blend_bitmap = models.BooleanField()
    duration = models.FloatField(blank = True, null = True)