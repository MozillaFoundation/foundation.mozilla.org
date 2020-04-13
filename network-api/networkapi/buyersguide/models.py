from django.db import models

from .pagemodels.get_product_image_upload_path import (
    get_product_image_upload_path
)

from .pagemodels.voting import (
    ProductVote,
    RangeProductVote,
    BooleanProductVote,
    VoteBreakdown,
    BooleanVoteBreakdown,
    RangeVoteBreakdown,
    Vote,
    BooleanVote,
    RangeVote,
)

from .pagemodels.products.original import (
    CloudinaryImageField,
    Product,
)

from .pagemodels.privacy import (
    ProductPrivacyPolicyLink
)

from .pagemodels.product_category import (
    BuyersGuideProductCategory
)


class Update(models.Model):
    source = models.URLField(
        max_length=2048,
        help_text='Link to source',
        blank=True,
    )

    title = models.CharField(
        max_length=256,
        blank=True,
    )

    author = models.CharField(
        max_length=256,
        blank=True,
    )

    snippet = models.TextField(
        max_length=5000,
        blank=True,
    )

    def __str__(self):
        return self.title


__all__ = [
    get_product_image_upload_path,
    BooleanProductVote,
    BooleanVote,
    BooleanVoteBreakdown,
    BuyersGuideProductCategory,
    CloudinaryImageField,
    Product,
    ProductPrivacyPolicyLink,
    ProductVote,
    RangeProductVote,
    RangeVote,
    RangeVoteBreakdown,
    Update,
    Vote,
    VoteBreakdown,
]
