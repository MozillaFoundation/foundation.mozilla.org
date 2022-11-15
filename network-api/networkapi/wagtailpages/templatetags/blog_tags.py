from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_root_or_page(context):
    root = context.get("root", None)
    page = context.get("page", None)

    if root:
        return root.specific
    elif page:
        return page.get_parent().specific
    else:
        print("There is no root or page in templatetag get_root_or_page")
