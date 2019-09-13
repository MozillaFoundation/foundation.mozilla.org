from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_root_or_page(context):
    root = context.get('root', None)
    page = context.get('page', None)

    if root:
        return root.specific
    else:
        return page.get_parent().specific
