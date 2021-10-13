from django import template
from django.conf import settings

register = template.Library()


# This method is used to keep track of the signup block to show it after a wide streamfield is used on a 2 column template
@register.simple_tag(takes_context=True)
def shown_signup_block(context, boolean):
    context["signup_shown"] = boolean
    return ''
