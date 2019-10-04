from .models import (
    ModularPage,
    MiniSiteNameSpace,
    PrimaryPage,
    IndexPage,
    NewsPage,
    InitiativesPage,
    ParticipatePage2,
    Styleguide,
    Homepage,
    RedirectingPage,

    BanneredCampaignPage,
    CampaignPage,
    OpportunityPage,
    BlogPage,
    YoutubeRegretsPage,

    CTA,
    Petition,
    Signup,

    # DEPRECATED
    ParticipatePage,
    PeoplePage,
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
        'share_link',
        'share_link_text',
        'share_twitter',
        'share_facebook',
        'share_email',
        'thank_you',
    )


@register(Signup)
class SignupTR(TranslationOptions):
    fields = (
    )


@register(PrimaryPage)
class PrimaryPageTR(TranslationOptions):
    fields = (
        'header',
        'intro',
        'body',
    )


@register(BanneredCampaignPage)
class BanneredCampaignPageTR(TranslationOptions):
    fields = (
    )


@register(IndexPage)
class IndexPageTR(TranslationOptions):
    fields = (
        'header',
        'intro',
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
        'hero_image',
    )


@register(RedirectingPage)
class RedirectingPageTR(TranslationOptions):
    fields = (
        'URL',
    )

# The following bindings are obsolete and require cleanup


@register(ParticipatePage)
class ParticipatePageTR(TranslationOptions):
    fields = ()


@register(PeoplePage)
class PeoplePageTR(TranslationOptions):
    fields = ()


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        'author',
        'body',
    )


@register(YoutubeRegretsPage)
class YoutubeRegretsPageTR(TranslationOptions):
    fields = {
        'headline',
        'intro_text',
        'intro_images',
        'faq',
        'regret_stories',
    }
