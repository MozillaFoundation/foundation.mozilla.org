from django.db import models


class OrderableRelationQuerySet(models.QuerySet):
    def related_items(self):
        """
        Return list of the related items instead of the through model.

        When working with Orderable models, we often use them to connect one model to
        another. For example: related articles on an article page. When displaying that
        information on the frontend, we are usually interested in the related item and
        not in the Orderable. But, the related manager usually only gives us access to
        the through model it self. This means we usually need to iterate over the
        orderables and access the related models from each instance of the orderable.
        That is inconvenient and it's odd to think about the orderables in the
        templates.

        This method gives access to a list of the related items directly. The
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

        """
        related_field_name = self.model.related_item_field_name

        items = [
            getattr(item, related_field_name)
            for item
            in self.select_related(related_field_name).all()
        ]

        return items
