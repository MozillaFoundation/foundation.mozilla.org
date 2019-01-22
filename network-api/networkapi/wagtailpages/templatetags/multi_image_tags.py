from django import template

register = template.Library()

@register.inclusion_tag('wagtailpages/tags/picture_ratios.html')
def optimize_images(image, class_names=""):
    return { 
        'unoptimized_image': image, 
        'class_names': class_names
    }