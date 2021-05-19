from django import template
from bs4 import BeautifulSoup
from wagtail.images.models import Image

register = template.Library()


@register.inclusion_tag('wagtailpages/tags/card.html')
def card(image, title, description, link_url, link_label):
    parsedDescription = BeautifulSoup(description, 'html.parser')

    image_url = image
    if isinstance(image, Image):
        # Check to see if the incoming image is a Wagtail image. We use this
        # for legacy {% card .. %} template tag support
        image_url = image.get_rendition('fill-350x197').url

    return {
        'image': image_url,
        'title': title,
        'description': description,
        'description_is_rich_text': len(parsedDescription.find_all(True)) > 0,
        'link_url': link_url,
        'link_label': link_label,
    }


@register.inclusion_tag('wagtailpages/tags/card-cta.html')
def cardCTA(
    image,
    title,
    description,
    link_url,
    link_label,
    facebook=None,
    twitter=None,
    email_subject=None,
    email_body=None
):

    return {
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label,
        'facebook': facebook,
        'twitter': twitter,
        'email_subject': email_subject,
        'email_body': email_body,
    }


@register.inclusion_tag('wagtailpages/tags/card-large.html')
def cardLarge(image, title, description, link_url, link_label):
    return {
        'image': image,
        'title': title,
        'description': description,
        'link_url': link_url,
        'link_label': link_label,
    }
