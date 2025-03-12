from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def environment_prefix(context):
    env_prefix = ""
    app_env = get_app_environment()
    if app_env == "Staging":
        env_prefix = "[S]"
    elif app_env == "Review":
        env_prefix = "[RA]"
    return env_prefix


@register.simple_tag(takes_context=True)
def onetrust_data_domain(context):
    """
    Get the OneTrust cookie "data-domain-script" script attribute.

    Data domain is taken from the data-domain-script script attribute via
    OneTrust's cookie script integration. While the test / production data
    domain id currently only differ by a suffix, this may change in the future
    """
    request = context.get("request")

    # TODO this can get cleaned up to use the mozfest site id
    # but depends on re-design if the site id will remain the same. Use domains for now.
    mozfest_domains = {
        "www.mozillafestival.org",
        "mozillafestival.mofostaging.net",
        "mozfest.localhost:8000",
    }

    if request.get_host().lower() in mozfest_domains:
        data_domain = "0193d09a-b154-785d-9623-61f75caff27f"
    else:
        data_domain = "0191beda-31c8-76ff-9093-4055176ccf8c"

    if get_app_environment() == "Production":
        return data_domain
    else:
        return data_domain + "-test"


def get_app_environment():
    return settings.APP_ENVIRONMENT
