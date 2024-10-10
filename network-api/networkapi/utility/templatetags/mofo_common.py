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


@register.simple_tag()
def onetrust_data_domain():
    """
    Get the OneTrust cookie "data-domain-script" script attribute.

    Data domain is taken from the data-domain-script script attribute via
    OneTrust's cookie script integration. We have two scripts & properties set up
    in OneTrust. One for production (foundation.mozilla.org) and one for
    dev/staging (foundation.mofostaging.net).
    """

    if get_app_environment() == "Production":
        return "0191beda-31c8-76ff-9093-4055176ccf8c"
    else:
        return "0190e65a-dbec-7548-89af-4b67155ee70a-test"


def get_app_environment():
    return settings.APP_ENVIRONMENT
