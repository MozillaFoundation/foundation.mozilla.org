from django.db import models

from wagtail.core import models as wagtail_models
from wagtail.snippets import models as snippet_models


@snippet_models.register_snippet
class BuyersGuideContentCategory(wagtail_models.TranslatableMixin, models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)

    class Meta(wagtail_models.TranslatableMixin.Meta):
        verbose_name = 'Buyers Guide Content Category'
        verbose_name_plural = 'Buyers Guide Content Categories'

    def __str__(self) -> str:
        return self.title

