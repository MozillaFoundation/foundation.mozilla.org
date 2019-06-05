from django import template

register = template.Library()


@register.simple_tag(name='primary_active_nav')
def primary_active_nav(request, root_path, target_path):

    if not request:
        return ""

    if target_path == root_path:
        return "active" if request.path == target_path else ""

    return "active" if request.path.startswith(target_path) else ""
