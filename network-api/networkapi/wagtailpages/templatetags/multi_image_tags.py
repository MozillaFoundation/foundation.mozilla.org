from django import template

register = template.Library()


@register.inclusion_tag('wagtailpages/tags/picture_ratios.html')
def optimize_images(image, aspect_ratio='16:9'):
    image_ratios = {
        'large': ['540x304', '1080x608'],
        'medium': ['480x270', '960x520'],
        'small': ['320x180', '640x360']
    }
    if aspect_ratio == '1:1':
        image_ratios = {
            'large': ['160x160', '320x320'],
            'small': ['92x92', '184x184']
        }

    for key, value in image_ratios.items():
        value[:] = ['fill-' + ratio + '-c0' for ratio in value]

    return {
        image_ratios: image_ratios,
        'unoptimized_image': image
    }
