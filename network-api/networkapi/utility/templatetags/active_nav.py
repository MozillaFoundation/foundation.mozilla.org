from django import template

register = template.Library()

@register.simple_tag(name='active_nav')
def active_nav(request, view_name):

    from django.core.urlresolvers import resolve, Resolver404
    path = resolve(request.path_info)
    if not request:
        return ""
    try:
        return "active" if path.url_name == view_name else ""
    except Resolver404:
        return ""
