from django import template

register = template.Library()


@register.simple_tag(name="primary_active_nav")
def primary_active_nav(request, root_url, target_url):
    if not request:
        return ""

    request_url = request.build_absolute_uri()

    # In order to work around https://github.com/wagtail/wagtail/issues/5379
    # we need to strip all protocols from the urls first, because they might
    # mismatch, even though they reasonably shouldn't.
    root_url = root_url.replace("http://", "").replace("https://", "")
    target_url = target_url.replace("http://", "").replace("https://", "")
    request_url = request_url.replace("http://", "").replace("https://", "")

    if target_url == root_url:
        return "active" if request_url == target_url else ""

    return "active" if request_url.startswith(target_url) else ""
