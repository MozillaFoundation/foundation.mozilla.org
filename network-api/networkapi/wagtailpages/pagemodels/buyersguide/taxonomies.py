from django.db import models

from wagtail.snippets import models as snippet_models


@snippet_models.register_snippet
class BuyersGuideContentCategory(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = 'Buyers Guide Content Category'
        verbose_name_plural = 'Buyers Guide Content Categories'

