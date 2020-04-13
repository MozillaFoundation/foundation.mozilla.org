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

from .pagemodels.cloudinary_image_field import (
    CloudinaryImageField
)

from .pagemodels.products.original import (
    Product,
)

from .pagemodels.products.base import (
    BaseProduct,
)

from .pagemodels.products.general import (
    GeneralProduct,
)

from .pagemodels.products.software import (
    SoftwareProduct,
)

from .pagemodels.privacy import (
    ProductPrivacyPolicyLink,
    BaseProductPrivacyPolicyLink,
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
    BaseProduct,
    BooleanProductVote,
    BooleanVote,
    BooleanVoteBreakdown,
    BuyersGuideProductCategory,
    CloudinaryImageField,
    GeneralProduct,
    Product,
    ProductPrivacyPolicyLink,
    ProductVote,
    RangeProductVote,
    RangeVote,
    RangeVoteBreakdown,
    SoftwareProduct,
    Update,
    Vote,
    VoteBreakdown,
]
