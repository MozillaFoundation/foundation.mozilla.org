from django import template
from django.utils import text as text_utils
from wagtail.contrib.routable_page.templatetags import wagtailroutablepage_tags

register = template.Library()


@register.simple_tag(takes_context=True)
def routableprofileurl(context, page, profile, *args, url_name="profile_route", **kwargs):
    '''
    Get URL of the profile route on a given page.

    This is a wrapper around Wagtail's `routablepageurl` and meant to be used with
    `RoutableProfileMixin`.

    '''
    return wagtailroutablepage_tags.routablepageurl(
        context=context,
        page=page,
        url_name=url_name,
        profile_id=profile.id,
        profile_slug=text_utils.slugify(profile.name),
        *args,
        **kwargs,
    )

