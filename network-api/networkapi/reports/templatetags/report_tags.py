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


@register.inclusion_tag("tags/reports/render_block_content_types.html")
def page_types_block(content_types):
    truncated = []
    count_remaining = 0
    if len(content_types) > 3:
        truncated = content_types[3:]
        content_types = content_types[:3]
        count_remaining = len(truncated)
    return {
        "content_types_truncated": content_types,
        "content_types_remaining": truncated,
        "count_remaining": count_remaining,
    }


@register.inclusion_tag("tags/reports/block_name.html")
def block_name(page_block):
    full_name = page_block["block"]
    short_name = full_name.split(".")[-1]
    return {
        "full_name": full_name,
        "short_name": short_name,
    }
