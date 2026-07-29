# Validates whether a string is either a valid URL, a query string (?param=test), or both.
url_or_query_regex = r"^(https?://[\w.-]+(/\S*)?)?(\?[\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$"

# Defualt rich text features
DEFAULT_RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "large",
    "ol",
    "ul",
    "hr",
    "embed",
    "link",
    "document-link",
    "image",
]

# Rich text features for basic formatting options
RICH_TEXT_BASE_OPTIONS = ["bold", "italic", "link"]

# Rich text features for the notice banner snippet. Headings are capped at h4 so a
# notice never competes with the page's own h1-h3 outline, and block-level embeds
# (image/embed/hr) are omitted because the banner is a single compact banner.
NOTICE_BANNER_RICH_TEXT_FEATURES = [
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "ol",
    "ul",
    "link",
    "document-link",
]
