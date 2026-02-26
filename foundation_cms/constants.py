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
