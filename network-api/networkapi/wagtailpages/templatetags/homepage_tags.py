from django import template
from django.conf import settings

register = template.Library()


# A special tag for homepage images that use the correct URL, because S3 troubles
@register.inclusion_tag('wagtailpages/tags/homepage_image.html', takes_context=True)
def homepage_image(context, path):
    return homepage_image_with_class(context, path, '')


# A special tag for homepage images that use the correct URL, because S3 troubles
@register.inclusion_tag('wagtailpages/tags/homepage_image.html', takes_context=True)
def homepage_image_with_class(context, path, classname):
    root = settings.MEDIA_URL

    if settings.USE_S3:
        awsl = settings.AWS_LOCATION
        awscd = settings.AWS_S3_CUSTOM_DOMAIN
        if awscd in root and awsl not in root:
            old = awscd
            new = awscd + '/' + awsl
            root = root.replace(old, new)

    url = '{}{}'.format(root, path)

    return {
        'url': url,
        'classname': classname,
    }
