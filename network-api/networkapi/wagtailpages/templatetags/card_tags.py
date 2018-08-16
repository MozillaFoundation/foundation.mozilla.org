from django import template

register = template.Library()


@register.inclusion_tag('wagtailpages/tags/card.html')
def card(image, title, description, link_url, link_label, commitment=None):
    return {
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label,
        'commitment': commitment,
    }

@register.inclusion_tag('wagtailpages/tags/card-cta.html')
def cardCTA(image, title, description, link_url, link_label, commitment=None):
    return {
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label,
        'commitment': commitment,
    }

@register.inclusion_tag('wagtailpages/tags/card-large.html')
def cardLarge(image, title, description, link_url, link_label, commitment=None):
    return {
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label,
        'commitment': commitment,
    }
