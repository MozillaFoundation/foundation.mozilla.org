# Validates whether a string is either a valid URL, a query string (?param=test), or both.
url_or_query_regex = r"^(https?://[\w.-]+(/\S*)?)?(\?[\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$"
