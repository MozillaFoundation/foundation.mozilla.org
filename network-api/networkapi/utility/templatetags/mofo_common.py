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
    Returns the appropriate OneTrust data-domain-script value based on the current domain.
    Falls back to test domain in non-production or unknown domains.
    """
    request = context.get("request")
    host = request.get_host().lower()

    # Mapping of domains to their OneTrust data-domain-script values
    domain_map = {
        "www.mozillafoundation.org": "01962092-7c56-70c5-851b-fb18cb7e7080",
        "prod.mozillafoundation.org": "01962091-75d4-77b1-ac68-ce829d931ae7",
        "foundation.mozilla.org": "0191beda-31c8-76ff-9093-4055176ccf8c",
        # MozFest domains
        "www.mozillafestival.org": "0193d09a-b154-785d-9623-61f75caff27f",
        "mozfest.mofostaging.net": "0193d09a-b154-785d-9623-61f75caff27f-test",
        "mozfest.localhost:8000": "0193d09a-b154-785d-9623-61f75caff27f-test",
    }

    env = get_app_environment()
    data_domain = domain_map.get(host)

    # Fallback for unknown domains or non-production environments
    if not data_domain:
        if env != "Production":
            return "01962092-7c56-70c5-851b-fb18cb7e7080-test"

    return data_domain


def get_app_environment():
    return settings.APP_ENVIRONMENT
