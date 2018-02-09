from django import template

register = template.Library()


@register.simple_tag(name='fellowship_active_nav')
def fellowship_active_nav(request, view_name):

    from django.core.urlresolvers import resolve, Resolver404
    path = resolve(request.path_info)
    if not request:
        return ""
    try:
        matched = [vn for vn in view_name.split() if path.url_name == vn]

        return "active" if matched else ""

    except Resolver404:
        return ""
