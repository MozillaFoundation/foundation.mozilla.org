from django import template

from foundation_cms.blocks.sections import group_into_sections

register = template.Library()


@register.simple_tag
def get_sections(stream_value):
    """
    Usage: {% get_sections page.body as sections %}
    """
    return group_into_sections(stream_value)
