from wagtail_ab_testing.models import AbTest
from wagtail_ab_testing.utils import request_is_trackable


@register.inclusion_tag("wagtail_ab_testing/script.html", takes_context=True)
def wagtail_ab_testing_script(context):
    request = context["request"]
    serving_variant = getattr(request, "wagtail_ab_testing_serving_variant", False)

    return {
        "request": request,
        "track": request_is_trackable(request),
        "page": context.get("page", None),
        "test": getattr(request, "wagtail_ab_testing_test", None),
        "version": AbTest.VERSION_VARIANT if serving_variant else AbTest.VERSION_CONTROL,
    }
