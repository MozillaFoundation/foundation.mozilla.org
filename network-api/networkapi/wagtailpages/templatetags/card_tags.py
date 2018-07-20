from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('wagtailpages/tags/card.html')
def card(md_width, image, title, description, link_url, link_label):
    return {
        'md_width': md_width,
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label
    }
