from django import template

register = template.Library()


@register.filter
def yes_no(value):
    """Converts boolean to yes or no string"""
    if value is None:
        return "Unknown"
    # Python doesn't have a ternary, so we rely on
    # type coercion to turn False into 0 and True
    # into 1, and using that as list index.
    return ("No", "Yes")[value]


@register.filter
def extended_yes_no(value):
    """Converts quad-state to human readable string"""
    if value == 'U':
        return 'Unknown'
    if value == 'NA':
        return 'N/A'
    return value
