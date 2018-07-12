from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name='settings_value')
def settings_value(key):
    return settings.__getattr__(str(key))
