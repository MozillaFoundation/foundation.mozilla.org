from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db import models


def get_related_items(
    queryset: "models.QuerySet", related_item_field: str, order_by: str = None
) -> list["models.Model"]:
    """
    Return list of the related items from the queryset.

    For each item in the queryset, the related item stored in `related_item_field` is
    returned.

    """
    # Apply ordering if needed
    if order_by:
        queryset = queryset.order_by(order_by)

    return [getattr(relation, related_item_field) for relation in queryset.select_related(related_item_field)]
