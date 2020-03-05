from .models import (
    MozfestHomepage,
    MozfestPrimaryPage,
)

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(MozfestPrimaryPage)
class MozfestPrimaryPageTR(TranslationOptions):
    fields = (
        'header',
        'intro',
        'body',
    )


@register(MozfestHomepage)
class MozfestHomepageTR(TranslationOptions):
    fields = (
        'cta_button_label',
        'banner_heading',
        'banner_guide_text',
        'banner_video_url',
    )
