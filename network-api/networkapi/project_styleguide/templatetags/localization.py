from pattern_library.monkey_utils import override_tag

from networkapi.wagtailpages.templatetags.localization import register

override_tag(register, name="get_unlocalized_url", default_html="/dummy")
override_tag(register, name="relocalized_url", default_html="/en/dummy")
override_tag(register, name="localizedroutablepageurl", default_html="/en/routed-dummy")
