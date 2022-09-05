from django.db import models


def get_related_items(
    queryset: models.QuerySet,
    related_item_field: str
) -> list[models.Model]:
    """
    Return list of the related items from the queryset.

    For each item in the queryset, the related item stored in `related_item_field` is
    returned.

    """
    return [
        getattr(relation, related_item_field)
        for relation
        in queryset.select_related(related_item_field)
    ]
