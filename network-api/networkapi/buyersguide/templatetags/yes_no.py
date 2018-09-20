from django import template

register = template.Library()


@register.filter
def yes_no(value):
    """Converts boolean to yes or no string"""
    return ("No", "Yes")[value]
