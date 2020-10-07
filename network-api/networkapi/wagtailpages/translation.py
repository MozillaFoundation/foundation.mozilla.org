from .models import (
    ModularPage,
    MiniSiteNameSpace,
    PrimaryPage,

    IndexPage,
    BlogIndexPage,
    CampaignIndexPage,

    NewsPage,
    InitiativesPage,
    ParticipatePage2,
    Styleguide,
    Homepage,
    FocusArea,
    RedirectingPage,

    BanneredCampaignPage,
    CampaignPage,
    OpportunityPage,
    BlogPage,
    YoutubeRegretsPage,
    YoutubeRegretsReporterPage,
    ArticlePage,
    PublicationPage,
    CTA,
    Petition,
    Signup,

    # DEPRECATED
    PeoplePage,
)

from .pagemodels.base import (
    HomepageTakeActionCards,
    PartnerLogos,
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


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    fields = ()


@register(CampaignIndexPage)
class CampaignIndexPageTR(TranslationOptions):
    fields = ()


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
        'hero_button_text',
        'hero_button_url',
        'hero_image',
        'cause_statement',
        'cause_statement_link_text',
        'quote_image',
        'quote_text',
        'quote_source_name',
        'quote_source_job_title',
        'partner_heading',
        'partner_intro_text',
        'partner_page_text',
        'take_action_title',
        'spotlight_headline',
    )


@register(FocusArea)
class FocusAreaTR(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(HomepageTakeActionCards)
class HomepageTakeActionCardsTR(TranslationOptions):
    fields = (
        'text',
    )


@register(PartnerLogos)
class PartnerLogosTR(TranslationOptions):
    fields = (
        'name',
    )


@register(RedirectingPage)
class RedirectingPageTR(TranslationOptions):
    fields = (
        'URL',
    )


@register(PublicationPage)
class PublicationPageTR(TranslationOptions):
    fields = ()


@register(ArticlePage)
class ArticlePageTR(TranslationOptions):
    fields = ()


# The following bindings are obsolete and require cleanup
@register(PeoplePage)
class PeoplePageTR(TranslationOptions):
    fields = ()


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
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


@register(YoutubeRegretsReporterPage)
class YoutubeRegretsReporterPageTR(TranslationOptions):
    fields = {
        'headline',
        'intro_text',
        'intro_images',
    }
