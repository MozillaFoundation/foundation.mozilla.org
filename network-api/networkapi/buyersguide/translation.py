from .models import (
    BuyersGuideProductCategory,
)

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(BuyersGuideProductCategory)
class BuyersGuideProductCategoryTR(TranslationOptions):
    fields = (
        'name',
    )
