from django import template

register = template.Library()

@register.simple_tag()
def fieldname(instance, field_name):
    return instance.get_verbose_field_name(field_name)