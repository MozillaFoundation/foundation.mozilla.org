from django.db import models
from django.utils.text import slugify

from wagtail.snippets.models import register_snippet

from .products.base import Product


@register_snippet
class BuyersGuideProductCategory(models.Model):
    """
    A simple category class for use with Buyers Guide products,
    registered as snippet so that we can moderate them if and
    when necessary.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(
        max_length=300,
        help_text='Description of the product category. Max. 300 characters.',
        blank=True
    )

    featured = models.BooleanField(
        default=False,
        help_text='Featured category will appear first on Buyer\'s Guide site nav'
    )

    hidden = models.BooleanField(
        default=False,
        help_text='Hidden categories will not appear in the Buyer\'s Guide site nav at all'
    )

    slug = models.SlugField(
        blank=True,
        help_text='A URL-friendly version of the product name. This is an auto-generated field.'
    )

    @property
    def published_product_count(self):
        return Product.objects.filter(product_category=self, draft=False).count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BuyersGuideProductCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Buyers Guide Product Category"
        verbose_name_plural = "Buyers Guide Product Categories"
