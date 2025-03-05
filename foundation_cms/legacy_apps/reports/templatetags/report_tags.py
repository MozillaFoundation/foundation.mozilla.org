from django import template
from django.urls import reverse
from django.utils.html import format_html, mark_safe

register = template.Library()


@register.simple_tag
def render_content_type(content_type):
    """Render a Content Type with a link to the content type's admin page"""
    return format_html(
        "<a href='{}'>{}</a>",
        reverse(
            "wagtailadmin_pages:type_use",
            kwargs={
                "content_type_app_name": content_type.app_label,
                "content_type_model_name": content_type.model,
            },
        ),
        content_type.name.title(),
    )


@register.simple_tag
def render_content_types(content_types):
    """Render a list of content types"""
    return mark_safe(", ".join([render_content_type(content_type) for content_type in content_types]))


@register.inclusion_tag("tags/reports/page_types_block.html")
def page_types_block(content_types):
    content_types_hidden = []
    count_hidden = 0
    if len(content_types) > 3:
        content_types_hidden = content_types[3:]
        content_types = content_types[:3]
        count_hidden = len(content_types_hidden)
    return {
        "content_types_shown": content_types,
        "content_types_hidden": content_types_hidden,
        "count_hidden": count_hidden,
    }


@register.inclusion_tag("tags/reports/block_name.html")
def block_name(page_block):
    full_name = page_block["block"]
    short_name = full_name.split(".")[-1]
    return {
        "full_name": full_name,
        "short_name": short_name,
    }
