from django import template

register = template.Library()


@register.simple_tag(name='primary_active_nav')
def primary_active_nav(request, root_url, target_url):

    if not request:
        return ""

    request_url = request.build_absolute_uri()

    if target_url == root_url:
        return "active" if request_url == target_url else ""


    return "active" if request_url.startswith(target_url) else ""
