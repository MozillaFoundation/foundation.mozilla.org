from django.db import models
from django.utils import text as text_utils

from wagtail.core import models as wagtail_models
from wagtail.snippets import models as snippet_models


@snippet_models.register_snippet
class BuyersGuideContentCategory(wagtail_models.TranslatableMixin, models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(null=False, blank=True)

    class Meta(wagtail_models.TranslatableMixin.Meta):
        verbose_name = 'Buyers Guide Content Category'
        verbose_name_plural = 'Buyers Guide Content Categories'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = text_utils.slugify(self.title)
        super().save(*args, **kwargs)
