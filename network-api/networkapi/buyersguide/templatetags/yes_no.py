from django import template

register = template.Library()


@register.filter
def yes_no(value):
    """Converts boolean to yes or no string"""
    if value is None:
        return "?"
    else:
        return ("No", "Yes")[value]
