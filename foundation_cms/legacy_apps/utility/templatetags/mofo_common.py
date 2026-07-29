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


def get_app_environment():
    return settings.APP_ENVIRONMENT
