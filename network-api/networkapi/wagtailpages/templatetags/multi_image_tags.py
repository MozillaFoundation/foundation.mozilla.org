from django import template

register = template.Library()

#  16:9 Aspect ratio image tag

@register.inclusion_tag('wagtailpages/tags/wide_image.html')
def wide_image(image, container_class_names=''):
    return {
        'unoptimized_image': image,
        'container_class_names': container_class_names
    }
