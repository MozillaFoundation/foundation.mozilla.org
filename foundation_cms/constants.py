# Validates whether a string is either a valid URL, a query string (?param=test), or both.
url_or_query_regex = r"^(https?://[\w.-]+(/\S*)?)?(\?[\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$"

# Rich text features for basic formatting options
RICH_TEXT_BASE_OPTIONS = ["bold", "italic", "link"]
