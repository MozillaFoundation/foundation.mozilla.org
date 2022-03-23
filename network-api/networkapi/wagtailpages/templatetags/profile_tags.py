from django import template
from django.utils import text as text_utils
from wagtail.contrib.routable_page.templatetags import wagtailroutablepage_tags

register = template.Library()


@register.simple_tag(takes_context=True)
def routableprofileurl(context, *args, page, profile, url_name="profile_route", **kwargs):
    '''
    Get URL of the profile route on a given page.

    This is a wrapper around Wagtail's `routablepageurl`. It passes the profiles id as `profile_id`
    and the slugified profile name as `profile_slug` to the url reveral. That means the urls should
    expect both these parameters. For example the route decorator could look something like this:

    ```
    @routable_models.route(r'^(?P<profile_id>[0-9]+)/(?P<profile_slug>[-a-z]+)/$')`
    def profile_route(self, request, profile_id, profile_slug):
        ...
    ```

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

