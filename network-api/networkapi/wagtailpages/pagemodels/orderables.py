from django.db import models


class OrderableRelationQuerySet(models.QuerySet):
    def related_items(self):
        field_name = self.model.related_item_field_name
        item_ids = self.values_list((f"{field_name}_id"), flat=True)

        field = getattr(self.model, field_name)
        return field.get_queryset().filter(id__in=item_ids)
