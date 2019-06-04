from django import template

register = template.Library()


@register.simple_tag(name='primary_active_nav')
def primary_active_nav(request, target_path):

    if not request:
        return ""

    # remove langauge code segment from path to make path comparison easier
    lang = f"/{request.LANGUAGE_CODE}"
    path_info = request.path_info[len(lang):] if request.path_info.startswith(lang) else request.path_info

    current = path_info.lstrip("/").rstrip("/").lower()
    target = target_path.lstrip("/").rstrip("/").lower()

    return "active" if current == target else ""
