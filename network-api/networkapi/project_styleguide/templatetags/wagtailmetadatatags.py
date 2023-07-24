from pattern_library.monkey_utils import override_tag
from wagtailmetadata.templatetags.wagtailmetadata_tags import register

override_tag(
    register,
    name="meta_tags",
    default_html='<title>Example title</title><meta name="description" content="Example description">',
)
