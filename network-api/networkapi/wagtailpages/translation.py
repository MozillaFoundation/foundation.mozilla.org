from .models import (
    ModularPage,
    MiniSiteNameSpace,
    PrimaryPage,
    NewsPage,
    InitiativesPage,
    ParticipatePage2,
    PeoplePage,
    Styleguide,
    Homepage,
    RedirectingPage,

    OpportunityPage,
    CampaignPage,

    CTA,
    Petition,
)

from .donation_modal import DonationModal

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(ModularPage)
class ModularPageTR(TranslationOptions):
    fields = (
        'header',
        'body',
    )


@register(MiniSiteNameSpace)
class MiniSiteNameSpaceTR(TranslationOptions):
    fields = ()


@register(CampaignPage)
class CampaignPageTR(TranslationOptions):
    fields = (
    )


@register(DonationModal)
class DonationModalTR(TranslationOptions):
    fields = (
        'name',
        'header',
        'body',
        'donate_text',
        'dismiss_text',
    )


@register(OpportunityPage)
class OpportunityPageTR(TranslationOptions):
    fields = (
    )


@register(CTA)
class CTATR(TranslationOptions):
    fields = (
        'name',
        'header',
        'description',
    )


@register(Petition)
class PetitionTR(TranslationOptions):
    fields = (
    )


@register(PrimaryPage)
class PrimaryPageTR(TranslationOptions):
    fields = (
        'header',
        'body',
    )


@register(NewsPage)
class NewsPageTR(TranslationOptions):
    fields = ()


@register(InitiativesPage)
class InitiativesPageTR(TranslationOptions):
    fields = ()


@register(ParticipatePage2)
class ParticipatePage2TR(TranslationOptions):
    fields = ()


@register(PeoplePage)
class PeoplePageTR(TranslationOptions):
    fields = ()


@register(Styleguide)
class StyleguideTR(TranslationOptions):
    fields = ()


@register(Homepage)
class HomepageTR(TranslationOptions):
    fields = (
        'hero_headline',
        'hero_story_description',
        'hero_button_text',
        'hero_button_url',
    )


@register(RedirectingPage)
class RedirectingPageTR(TranslationOptions):
    fields = (
        'URL',
    )
