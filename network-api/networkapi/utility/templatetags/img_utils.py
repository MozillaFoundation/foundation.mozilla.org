from django import template
from django.contrib.staticfiles.finders import find
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def include_svg(path):
    """Renders an SVG from the static directory."""
    if not path.endswith(".svg"):
        raise ValueError("Path must be to an SVG file.")

    absolute_path = find(path)

    if not absolute_path:
        raise ValueError("SVG file not found.")

    with open(absolute_path, "r") as f:
        return format_html(f.read())
