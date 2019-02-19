from django import template

register = template.Library()

#  16:9 Aspect ratio image tag

@register.inclusion_tag('wagtailpages/tags/wide_image.html')
def wide_image(image, container_class_names=''):
    return {
        'unoptimized_image': image,
        'container_class_names': container_class_names
    }

#  1:1 Aspect ratio image tag

@register.inclusion_tag('wagtailpages/tags/square_image.html')
def square_image(image, container_class_names='', img_class_names=''):
    return {
        'unoptimized_image': image,
        'pic_class_names': container_class_names,
        'pic_img_class_names': img_class_names
    }
