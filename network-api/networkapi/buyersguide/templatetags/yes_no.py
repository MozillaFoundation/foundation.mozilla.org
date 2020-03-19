from django import template
from django.utils.translation import gettext

register = template.Library()


@register.filter
def yes_no(value):
    """Converts boolean to yes or no string"""
    if value is None:
        return gettext('Unknown')
    # Python doesn't have a ternary, so we rely on
    # type coercion to turn False into 0 and True
    # into 1, and using that as list index.
    return (gettext('No'), gettext('Yes'))[value]


@register.filter
def extended_yes_no(value):
    """Converts quad-state to human readable string"""
    if value == 'U':
        return gettext('Unknown')
    if value == 'NA':
        return gettext('N/A')
    if value == 'Yes':
        return gettext('Yes')
    if value == 'No':
        return gettext('No')
    return value
