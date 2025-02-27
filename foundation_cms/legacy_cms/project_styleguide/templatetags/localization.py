from pattern_library.monkey_utils import override_tag

from legacy_cms.wagtailpages.templatetags.localization import register

# Override the localization tags with a fake implementation to return dummy URLs.
# The fake implementation will only be used when viewing the pattern library.
# See https://torchbox.github.io/django-pattern-library/guides/overriding-template-tags/
#
# These tags are used in a large number of pages, and their output does
# not affect appearance. Overriding them centrally here is a convenient way
# to avoid having to override the tags in each individual YAML file.
override_tag(register, name="get_unlocalized_url", default_html="/dummy")
