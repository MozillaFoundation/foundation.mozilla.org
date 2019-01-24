from django import template

register = template.Library()


@register.simple_tag(name='primary_active_nav')
def primary_active_nav(request, target_path):

    if not request:
        return ""

    # remove langauge code segment from path to make path comparison easier
    lang = f"/{request.LANGUAGE_CODE}"
    path_info = request.path_info[len(lang):] if request.path_info.startswith(lang) else request.path_info

    return "active" if path_info.rstrip("/") == target_path.rstrip("/") else ""
