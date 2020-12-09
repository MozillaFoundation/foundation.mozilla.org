from django import template

register = template.Library()


@register.inclusion_tag('wagtailpages/tags/picture_ratios.html')
def optimize_images(image):
    return {
        'unoptimized_image': image
    }


@register.simple_tag(name='custom_image_height')
def custom_image_height(image, height=410):
    """
    Automatically fill an image with 1400 by X pixels where X is a variable integer.

    If a height is not set (False or None) default to a 410px height as per the
    original design.
    """
    return image.get_rendition(f'fill-1400x{height}')
