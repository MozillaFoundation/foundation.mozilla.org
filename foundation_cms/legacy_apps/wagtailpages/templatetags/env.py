from django import template
from django.conf import settings

register = template.Library()


@register.filter
def env(value):
    if hasattr(settings, value):
        return getattr(settings, value)
    else:
        return ""
