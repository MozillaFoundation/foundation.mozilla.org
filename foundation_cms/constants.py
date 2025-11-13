# Validates whether a string is either a valid URL, a query string (?param=test), or both.
url_or_query_regex = r"^(https?://[\w.-]+(/\S*)?)?(\?[\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$"

# Rich text features excluding heading elements
RICH_TEXT_FEATURES_NO_HEADINGS = [
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
