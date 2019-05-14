from .models import (
    MozfestHomepage,
    MozfestPrimaryPage,
)

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(MozfestPrimaryPage)
class MozfestPrimaryPageTR(TranslationOptions):
    fields = ()


@register(MozfestHomepage)
class MozfestHomepageTR(TranslationOptions):
    fields = ()
