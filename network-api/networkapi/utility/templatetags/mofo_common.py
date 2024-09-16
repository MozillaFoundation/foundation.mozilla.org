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
    elif app_env == "Local":
        env_prefix = "[L]"
    return env_prefix


@register.simple_tag()
def onetrust_data_domain():
    """
    Get the OneTrust cookie "data-domain-script" script attribute.

    Data domain is taken from the data-domain-script script attribute via
    OneTrust's cookie script integration. While the test / production data
    domain id currently only differ by a suffix, this may change in the future
    """
    data_domain = "0190e65a-dbec-7548-89af-4b67155ee70a"
    if get_app_environment() == "Production":
        return data_domain
    else:
        return data_domain + "-test"


def get_app_environment():
    return settings.APP_ENVIRONMENT
