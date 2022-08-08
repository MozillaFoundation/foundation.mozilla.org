from django.db import models


class OrderableRelationQuerySet(models.QuerySet):
    def related_items(self):
        article_ids = self.values_list(('article_id'), flat=True)
        return self.model.article.get_queryset().filter(id__in=article_ids)

