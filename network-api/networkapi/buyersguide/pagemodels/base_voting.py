from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from networkapi.buyersguide.validators import ValueListValidator

from .products.base import BaseProduct


class BaseProductVote(models.Model):
    votes = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class BaseRangeProductVote(BaseProductVote):
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
        BaseProduct,
        on_delete=models.CASCADE,
        related_name='range_product_votes',
    )


class BaseBooleanProductVote(BaseProductVote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['confidence'])
        ]
    )
    product = models.ForeignKey(
        BaseProduct,
        on_delete=models.CASCADE,
        related_name='boolean_product_votes'
    )


class BaseVoteBreakdown(models.Model):
    count = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class BaseBooleanVoteBreakdown(BaseVoteBreakdown):
    product_vote = models.ForeignKey(
        BaseBooleanProductVote,
        on_delete=models.CASCADE
    )
    bucket = models.IntegerField(
        validators=[
            ValueListValidator(
                valid_values=[0, 1]
            )
        ]
    )


class BaseRangeVoteBreakdown(BaseVoteBreakdown):
    product_vote = models.ForeignKey(
        BaseRangeProductVote,
        on_delete=models.CASCADE
    )
    bucket = models.IntegerField(
        validators=[
            ValueListValidator(
                valid_values=[0, 1, 2, 3, 4]
            )
        ]
    )


class BaseVote(models.Model):
    product = models.ForeignKey('BaseProduct', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseBooleanVote(BaseVote):
    attribute = models.CharField(
        max_length=100,
        validators=[
            ValueListValidator(valid_values=['confidence'])
        ]
    )
    value = models.BooleanField()


class BaseRangeVote(BaseVote):
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
