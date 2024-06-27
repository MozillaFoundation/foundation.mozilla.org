from django import template
from wagtail.models import Locale

register = template.Library()


@register.simple_tag(takes_context=True)
def get_root_or_page(context):
    root = context.get("root", None)
    page = context.get("page", None)
    locale = Locale.get_active()

    if root:
        return root.get_translation_or_none(locale).specific
    elif page:
        return page.get_translation_or_none(locale).get_parent().specific
    else:
        print("There is no root or page in templatetag get_root_or_page")
