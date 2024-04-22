from pattern_library.monkey_utils import override_tag
from wagtail.contrib.routable_page.templatetags.wagtailroutablepage_tags import register

override_tag(register, name="routablepageurl", default_html="")
