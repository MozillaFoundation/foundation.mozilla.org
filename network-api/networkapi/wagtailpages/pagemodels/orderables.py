from django.db import models


class OrderableRelationQuerySet(models.QuerySet):
    def related_items(self):
        """
        Return QuerySet of the related items instead of the through model.

        When working with Orderable models, we often use them to connect one model to
        another. For example: related articles on an article page. When displaying that
        information on the frontend, we are usually interested in the related item and
        not in the Orderable. But, the related manager usually only gives us access to
        the through model it self. This means we usually need to iterate over the
        orderables and access the related models from each instance of the orderable.
        That is inconvenient and it's odd to think about the orderables in the
        templates.

        This method gives access to a queryset of the related items directly. The
        order defined by the orderable is kept.

        To make use of this method, you need to set this queryset as the manager for
        the Orderable through model and specify the name of the foreign key field
        from which the related items should be returned. Like so:

        ```python
        class OrderableRelation(Orderable):
            page = cluster_fields.ParentalKey(
                'ArticlePage',
                related_name='featured_article_relations',
            )
            article = models.ForeignKey(
                'ArticlePage',
                on_delete=models.CASCADE,
                null=False,
                blank=False,
            )

            panels = [PageChooserPanel('article', page_type='ArticlePage')]

            objects = orderables.OrderableRelationQuerySet.as_manager()
            related_item_field_name = "article"
        ```

        The foreign key field to the related item needs to have a `related_name`,
        otherwise we can not keep the ordering enforced, which would make the use
        of the orderable useless. You probably want to avoid name collisions, but
        apart from that the exact value of the `related_name` is not important. The
        easiest way is to just not define the `ralated_name` argument to the field
        definition, which will then get a default value.

        """
        related_field_name = self.model.related_item_field_name
        related_field = getattr(self.model, related_field_name)
        reverse_name = related_field.field.related_query_name()

        item_ids = self.values(related_field_name)

        items = related_field.get_queryset().order_by(
            f'{reverse_name}__sort_order',
        ).filter(pk__in=item_ids).distinct()

        return items
