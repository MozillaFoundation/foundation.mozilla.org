from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from networkapi.buyersguide.validators import ValueListValidator

from .products.base import Product


class ProductVote(models.Model):
    votes = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class RangeProductVote(ProductVote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['creepiness'])
        ]
    )
    average = models.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(100)
        )
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='range_product_votes',
    )


class BooleanProductVote(ProductVote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['confidence'])
        ]
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='boolean_product_votes'
    )


class VoteBreakdown(models.Model):
    count = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class BooleanVoteBreakdown(VoteBreakdown):
    product_vote = models.ForeignKey(
        BooleanProductVote,
        on_delete=models.CASCADE
    )
    bucket = models.IntegerField(
        validators=[
            ValueListValidator(
                valid_values=[0, 1]
            )
        ]
    )


class RangeVoteBreakdown(VoteBreakdown):
    product_vote = models.ForeignKey(
        RangeProductVote,
        on_delete=models.CASCADE
    )
    bucket = models.IntegerField(
        validators=[
            ValueListValidator(
                valid_values=[0, 1, 2, 3, 4]
            )
        ]
    )


class Vote(models.Model):
    # This is the only "BaseProduct" left, as "Product" is just a code alias for now.
    product = models.ForeignKey('BaseProduct', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BooleanVote(Vote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['confidence'])
        ]
    )
    value = models.BooleanField()


class RangeVote(Vote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['creepiness'])
        ]
    )
    value = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
