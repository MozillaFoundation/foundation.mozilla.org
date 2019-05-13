from .models import (
    MozfestHomepage,
)


from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(MozfestHomepage)
class MozfestHomepageTR(TranslationOptions):
    fields = ()
