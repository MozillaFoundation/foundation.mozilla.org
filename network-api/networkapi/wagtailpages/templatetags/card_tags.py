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
def cardCTA(image, title, description, link_url, link_label, commitment=None, facebook=None, twitter=None, email_subject=None, email_body=None):
    return {
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label,
        'commitment': commitment,
        'facebook': facebook,
        'twitter': twitter,
        'email_subject': email_subject,
        'email_body': email_body,
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
