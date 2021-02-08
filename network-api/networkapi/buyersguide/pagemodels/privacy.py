from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.core.models import TranslatableMixin
from wagtail_localize.fields import TranslatableField, SynchronizedField

from .products.base import Product


@register_snippet
class ProductPrivacyPolicyLink(TranslatableMixin, Orderable, models.Model):
    product = ParentalKey(
        Product,
        related_name='privacy_policy_links',
        on_delete=models.CASCADE
    )

    label = models.CharField(
        max_length=500,
        help_text='Label for this link on the product page'
    )

    url = models.URLField(
        max_length=2048,
        help_text='Privacy policy URL',
        blank=True
    )

    translatable_fields = [
        TranslatableField('label'),
        SynchronizedField('url'),
    ]

    def __str__(self):
        return f'{self.product.name}: {self.label} ({self.url})'

    class Meta:
        verbose_name = "Buyers Guide Product Privacy Policy link"
        verbose_name_plural = "Buyers Guide Product Privacy Policy links"
        app_label = "buyersguide"
        unique_together = ('translation_key', 'locale',)
