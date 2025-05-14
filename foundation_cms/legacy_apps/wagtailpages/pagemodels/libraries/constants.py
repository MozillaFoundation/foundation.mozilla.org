import collections

from django.utils.translation import gettext_lazy as _

# We don't want to expose the actual database column value that we use for sorting.
# Therefore, we need a separate value that is used in the form and url.
SortOption = collections.namedtuple("SortOption", ["label", "value", "order_by_value"])

SORT_NEWEST_FIRST = SortOption(
    label=_("Newest first"),
    value="newest-first",
    order_by_value="-original_publication_date",
)
SORT_OLDEST_FIRST = SortOption(
    label=_("Oldest first"),
    value="oldest-first",
    order_by_value="original_publication_date",
)
SORT_ALPHABETICAL = SortOption(
    label=_("Alphabetical (A-Z)"),
    value="alphabetical",
    order_by_value="title",
)
SORT_ALPHABETICAL_REVERSED = SortOption(
    label=_("Alphabetical (Z-A)"),
    value="alphabetical-reversed",
    order_by_value="-title",
)
SORT_CHOICES = {
    SORT_NEWEST_FIRST.value: SORT_NEWEST_FIRST,
    SORT_OLDEST_FIRST.value: SORT_OLDEST_FIRST,
    SORT_ALPHABETICAL.value: SORT_ALPHABETICAL,
    SORT_ALPHABETICAL_REVERSED.value: SORT_ALPHABETICAL_REVERSED,
}

LATEST_ARTICLES_COUNT = 3
