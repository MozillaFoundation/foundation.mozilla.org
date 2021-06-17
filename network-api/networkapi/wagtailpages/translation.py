# TODO: REmove this and other translation.py files.
# They aren't needed but keep coming back when we merge master into our localization branch
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
    DearInternetPage,
    OpportunityPage,
    BlogPage,
    YoutubeRegretsPage,
    YoutubeRegretsReporterPage,
    ArticlePage,
    PublicationPage,
    CTA,
    Petition,
    Signup,

    # Product Pages
    ProductPage,
    SoftwareProductPage,
    GeneralProductPage,
    BuyersGuidePage,

    # Product Page related
    ProductPagePrivacyPolicyLink,
)

from .pagemodels.base import (
    HomepageTakeActionCards,
    PartnerLogos,
)
from networkapi.wagtailpages.pagemodels.products import (
    BuyersGuideProductCategory,
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
    fields = (
        'subtitle',
        'secondary_subtitle',
        'additional_author_copy',
        'intro_notes',
        'notes',
        'contents_title',
    )


@register(ArticlePage)
class ArticlePageTR(TranslationOptions):
    fields = (
        'body',
        'subtitle',
        'secondary_subtitle',
    )


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


@register(ProductPage)
class ProductPageTR(TranslationOptions):
    fields = (
        'price',
        'blurb',
        'worst_case',
        'signup_requirement_explanation',
        'how_does_it_use_data_collected',
        'user_friendly_privacy_policy_helptext',
        'uses_encryption_helptext',
        'security_updates_helptext',
        'strong_password_helptext',
        'manage_vulnerabilities_helptext',
        'privacy_policy_helptext',
    )


@register(SoftwareProductPage)
class SoftwareProductPageTR(TranslationOptions):
    fields = ()


@register(GeneralProductPage)
class GeneralProductPageTR(TranslationOptions):
    fields = (
        'personal_data_collected',
        'biometric_data_collected',
        'social_data_collected',
        'how_can_you_control_your_data',
        'track_record_details',
        'offline_use_description',
        'ai_helptext',
    )


@register(BuyersGuidePage)
class BuyersGuidePageTR(TranslationOptions):
    fields = (
        'header',
        'intro_text',
    )


@register(ProductPagePrivacyPolicyLink)
class ProductPagePrivacyPolicyLinkTR(TranslationOptions):
    fields = (
        'label',
    )


@register(DearInternetPage)
class DearInternetPageTR(TranslationOptions):
    fields = {
        'intro_texts',
        'letters_section_heading',
        'letters',
        'cta',
        'cta_button_text',
        'cta_button_link'
    }


@register(BuyersGuideProductCategory)
class BuyersGuideProductCategoryTR(TranslationOptions):
    fields = (
        'name', 'description',
    )
