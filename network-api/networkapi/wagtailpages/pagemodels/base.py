from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Locale
from wagtail.models import Orderable as WagtailOrderable
from wagtail.models import Page, TranslatableMixin
from wagtail.search import index
from wagtail_ab_testing.models import AbTest
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.donate_banner.models import DonateBannerPage
from networkapi.wagtailpages.pagemodels.customblocks.link_block import LinkBlock

# TODO:  https://github.com/mozilla/foundation.mozilla.org/issues/2362
from ..donation_modal import DonationModals  # noqa: F401
from ..utils import CharCountWidget, get_page_tree_information
from .customblocks.base_fields import base_fields
from .customblocks.base_rich_text_options import base_rich_text_options
from .mixin.foundation_banner_inheritance import FoundationBannerInheritanceMixin
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from .mixin.foundation_navigation import FoundationNavigationPageMixin

hero_intro_heading_default_text = "A healthy internet is one in which privacy, openness, and inclusion are the norms."
hero_intro_body_default_text = (
    "Mozilla empowers consumers to demand better online privacy, trustworthy AI, "
    "and safe online experiences from Big Tech and governments. We work across "
    "borders, disciplines, and technologies to uphold principles like privacy, "
    "inclusion and decentralization online."
)


class BasePage(FoundationMetadataPageMixin, FoundationNavigationPageMixin, Page):
    class Meta:
        abstract = True

    def get_donate_banner(self, request):
        # Check if there's a DonateBannerPage.
        default_locale = Locale.get_default()
        donate_banner_page = DonateBannerPage.objects.filter(locale=default_locale).first()

        # If there is no DonateBannerPage or no donate_banner is set, return None.
        if not donate_banner_page or not donate_banner_page.donate_banner:
            return None

        # Check if the user has Do Not Track enabled by inspecting the DNT header.
        dnt_enabled = request.headers.get("DNT") == "1"

        # Check if there's an active A/B test for the DonateBannerPage.
        active_ab_test = AbTest.objects.filter(page=donate_banner_page, status=AbTest.STATUS_RUNNING).first()

        # If there's no A/B test found or DNT is enabled, return the page's donate_banner field as usual.
        if not active_ab_test or dnt_enabled:
            donate_banner = donate_banner_page.donate_banner.localized
            donate_banner.variant_version = "N/A"
            donate_banner.active_ab_test = "N/A"
            return donate_banner

        # Check for the cookie related to this A/B test.
        # In wagtail-ab-testing, the cookie name follows the format:
        # "wagtail-ab-testing_{ab_test.id}_version".
        # For details, see the source code here:
        # https://github.com/wagtail-nest/wagtail-ab-testing/blob/main/wagtail_ab_testing/wagtail_hooks.py#L196-L197
        test_cookie_name = f"wagtail-ab-testing_{active_ab_test.id}_version"
        test_version = request.COOKIES.get(test_cookie_name)

        # If no version cookie is found, grab a test version for the current user.
        if not test_version:
            test_version = active_ab_test.get_new_participant_version()

        if test_version == "variant":
            is_variant = True
        else:
            is_variant = False

        # Attach active test and variant flag to request for {% wagtail_ab_testing_script %} template tag.
        # This allows wagtail-ab-testing to track events for this test, and set the version cookie if needed.
        request.wagtail_ab_testing_test = active_ab_test
        request.wagtail_ab_testing_serving_variant = is_variant

        # Return the appropriate donate banner
        if is_variant:
            donate_banner = active_ab_test.variant_revision.as_object().donate_banner.localized
        else:
            donate_banner = donate_banner_page.donate_banner.localized

        donate_banner.variant_version = test_version
        donate_banner.active_ab_test = active_ab_test.name
        return donate_banner

    def get_context(self, request):
        context = super().get_context(request)
        context["donate_banner"] = self.get_donate_banner(request)
        return context


class PrimaryPage(FoundationBannerInheritanceMixin, BasePage):  # type: ignore
    """
    Basically a straight copy of modular page, but with
    restrictions on what can live 'under it'.

    Ideally this is just PrimaryPage(ModularPage) but
    setting that up as a migration seems to be causing
    problems.
    """

    # This page is deprecated. While we keep the existing pages around,
    # we don't want to create new ones.
    is_creatable = False

    header = models.CharField(max_length=250, blank=True)

    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_banner",
        verbose_name="Hero Image",
        help_text="Choose an image that's bigger than 4032px x 1152px with aspect ratio 3.5:1",
    )

    intro = models.CharField(
        max_length=350,
        blank=True,
        help_text="Intro paragraph to show in hero cutout box",
    )

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text="For text-heavy pages, turn this on to reduce the overall width of the content on the page.",
    )

    body = StreamField(base_fields, use_json_field=True)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("narrowed_page_content"),
            ],
            classname="collapsible",
        ),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("banner"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("header"),
        SynchronizedField("banner"),
        TranslatableField("intro"),
        TranslatableField("body"),
        SynchronizedField("narrowed_page_content"),
    ]

    subpage_types = [
        "PrimaryPage",
        "BanneredCampaignPage",
        "OpportunityPage",
        "ArticlePage",
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        context = get_page_tree_information(self, context)
        return context


class InitiativeSection(TranslatableMixin, models.Model):
    page = ParentalKey(
        "wagtailpages.InitiativesPage",
        related_name="initiative_sections",
    )

    sectionImage = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="section_image",
        verbose_name="Hero Image",
    )

    sectionHeader = models.CharField(
        verbose_name="Header",
        max_length=250,
    )

    sectionCopy = models.TextField(
        verbose_name="Subheader",
    )

    sectionButtonTitle = models.CharField(
        verbose_name="Button Text",
        max_length=250,
    )

    sectionButtonURL = models.TextField(
        verbose_name="Button URL",
    )

    sectionButtonTitle2 = models.CharField(verbose_name="Button 2 Text", max_length=250, blank="True")

    sectionButtonURL2 = models.TextField(verbose_name="Button 2 URL", blank="True")

    panels = [
        FieldPanel("sectionImage"),
        FieldPanel("sectionHeader"),
        FieldPanel("sectionCopy"),
        FieldPanel("sectionButtonTitle"),
        FieldPanel("sectionButtonURL"),
        FieldPanel("sectionButtonTitle2"),
        FieldPanel("sectionButtonURL2"),
    ]

    translatable_fields = [
        SynchronizedField("sectionImage"),
        TranslatableField("sectionHeader"),
        TranslatableField("sectionCopy"),
        TranslatableField("sectionButtonTitle"),
        SynchronizedField("sectionButtonURL"),
        TranslatableField("sectionButtonTitle2"),
        SynchronizedField("sectionButtonURL2"),
    ]


class InitiativesPage(PrimaryPage):
    template = "wagtailpages/static/initiatives_page.html"

    subpage_types = [
        "BanneredCampaignPage",
        "MiniSiteNameSpace",
        "OpportunityPage",
        # The following additional types are here to ensure
        # that the /initiatives route can house all the pages
        # that originally lived under /opportunity
        "BlogPage",
        "CampaignPage",
        "YoutubeRegretsPage",
        "ArticlePage",
    ]

    primaryHero = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_hero",
        verbose_name="Primary Hero Image",
    )

    subheader = models.TextField(
        blank=True,
    )

    h3 = models.TextField(
        blank=True,
    )

    sub_h3 = models.TextField(
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("primaryHero"),
        FieldPanel("header"),
        FieldPanel("subheader"),
        FieldPanel("h3"),
        FieldPanel("sub_h3"),
        InlinePanel("initiative_sections", label="Initiatives"),
        InlinePanel("featured_highlights", label="Highlights", max_num=9),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        SynchronizedField("primaryHero"),
        TranslatableField("header"),
        TranslatableField("subheader"),
        TranslatableField("h3"),
        TranslatableField("sub_h3"),
        TranslatableField("featured_highlights"),
        TranslatableField("initiative_sections"),
    ]

    @property
    def ordered_featured_highlights(self):
        return InitiativesHighlights.objects.filter(page=self).select_related("highlight").order_by("sort_order")


class ParticipatePage2(PrimaryPage):

    max_count = 1

    template = "wagtailpages/static/participate_page2.html"

    ctaHero = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_hero_participate",
        verbose_name="Primary Hero Image",
    )

    ctaHeroHeader = models.TextField(
        blank=True,
    )

    ctaHeroSubhead = RichTextField(
        features=base_rich_text_options,
        blank=True,
    )

    ctaButtonTitle = models.CharField(
        verbose_name="Button Text",
        max_length=250,
        blank=True,
    )

    ctaButtonURL = models.TextField(
        verbose_name="Button URL",
        blank=True,
    )

    ctaHero2 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_hero_participate2",
        verbose_name="Primary Hero Image",
    )

    ctaHeroHeader2 = models.TextField(
        blank=True,
    )

    ctaHeroSubhead2 = RichTextField(
        features=base_rich_text_options,
        blank=True,
    )

    ctaButtonTitle2 = models.CharField(
        verbose_name="Button Text",
        max_length=250,
        blank=True,
    )

    ctaButtonURL2 = models.TextField(
        verbose_name="Button URL",
        blank=True,
    )

    ctaHero3 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_hero_participate3",
        verbose_name="Primary Hero Image",
    )

    ctaHeroHeader3 = models.TextField(
        blank=True,
    )

    ctaHeroSubhead3 = RichTextField(
        features=base_rich_text_options,
        blank=True,
    )

    ctaFacebook3 = models.TextField(
        blank=True,
    )

    ctaTwitter3 = models.TextField(
        blank=True,
    )

    ctaEmailShareBody3 = models.TextField(
        blank=True,
    )

    ctaEmailShareSubject3 = models.TextField(
        blank=True,
    )

    h2 = models.TextField(
        blank=True,
    )

    h2Subheader = models.TextField(
        blank=True,
        verbose_name="H2 Subheader",
    )

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        SynchronizedField("ctaHero"),
        TranslatableField("ctaHeroHeader"),
        TranslatableField("ctaHeroSubhead"),
        TranslatableField("ctaButtonTitle"),
        TranslatableField("ctaButtonURL"),
        SynchronizedField("ctaHero2"),
        TranslatableField("ctaHeroHeader2"),
        TranslatableField("ctaHeroSubhead2"),
        TranslatableField("ctaButtonTitle2"),
        TranslatableField("ctaButtonURL2"),
        SynchronizedField("ctaHero3"),
        TranslatableField("ctaHeroHeader3"),
        TranslatableField("ctaHeroSubhead3"),
        TranslatableField("ctaFacebook3"),
        TranslatableField("ctaTwitter3"),
        TranslatableField("ctaEmailShareBody3"),
        TranslatableField("ctaEmailShareSubject3"),
        TranslatableField("h2"),
        TranslatableField("h2Subheader"),
        TranslatableField("featured_highlights"),
        TranslatableField("featured_highlights2"),
        TranslatableField("cta4"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("ctaHero"),
                FieldPanel("ctaHeroHeader"),
                FieldPanel("ctaHeroSubhead"),
                FieldPanel("ctaButtonTitle"),
                FieldPanel("ctaButtonURL"),
            ],
            heading="Primary CTA",
            classname="collapsible",
        ),
        FieldPanel("h2"),
        FieldPanel("h2Subheader"),
        InlinePanel("featured_highlights", label="Highlights Group 1", max_num=3),
        MultiFieldPanel(
            [
                FieldPanel("ctaHero2"),
                FieldPanel("ctaHeroHeader2"),
                FieldPanel("ctaHeroSubhead2"),
                FieldPanel("ctaButtonTitle2"),
                FieldPanel("ctaButtonURL2"),
            ],
            heading="CTA 2",
            classname="collapsible",
        ),
        InlinePanel("featured_highlights2", label="Highlights Group 2", max_num=6),
        MultiFieldPanel(
            [
                FieldPanel("ctaHero3"),
                FieldPanel("ctaHeroHeader3"),
                FieldPanel("ctaHeroSubhead3"),
                FieldPanel("ctaFacebook3"),
                FieldPanel("ctaTwitter3"),
                FieldPanel("ctaEmailShareSubject3"),
                FieldPanel("ctaEmailShareBody3"),
            ],
            heading="CTA 3",
            classname="collapsible",
        ),
        InlinePanel("cta4", label="CTA Group 4", max_num=3),
    ]

    @property
    def ordered_featured_highlights(self):
        return self.featured_highlights.select_related("highlight").order_by("sort_order")

    @property
    def ordered_featured_highlights2(self):
        return self.featured_highlights2.select_related("highlight").order_by("sort_order")


class Styleguide(PrimaryPage):
    max_count = 1

    template = "pages/styleguide.html"

    emoji_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Emoji style image for use in the styleguide.",
    )

    content_panels = PrimaryPage.content_panels + [
        FieldPanel("emoji_image"),
    ]

    subpage_types: list = []


class HomepageIdeasPosts(TranslatableMixin, WagtailOrderable):
    page = ParentalKey(
        "wagtailpages.Homepage",
        related_name="ideas_posts",
    )
    blog = models.ForeignKey("BlogPage", on_delete=models.CASCADE, related_name="+")
    cta = models.CharField(max_length=50, default="Read more")
    panels = [
        FieldPanel("blog"),
        FieldPanel("cta", heading="CTA Link Text"),
    ]

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return self.page.title + "->" + self.blog.title


class HomepageHighlights(TranslatableMixin, WagtailOrderable):
    page = ParentalKey(
        "wagtailpages.Homepage",
        related_name="highlights",
    )
    blog = models.ForeignKey("BlogPage", on_delete=models.CASCADE, related_name="+")
    panels = [
        FieldPanel("blog"),
    ]

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return self.page.title + "->" + self.blog.title


class InitiativesHighlights(TranslatableMixin, WagtailOrderable, models.Model):
    page = ParentalKey(
        "wagtailpages.InitiativesPage",
        related_name="featured_highlights",
    )
    highlight = models.ForeignKey("highlights.Highlight", on_delete=models.CASCADE, related_name="+")
    panels = [
        FieldPanel("highlight"),
    ]

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        verbose_name = "highlight"
        verbose_name_plural = "highlights"

    def __str__(self):
        return self.page.title + "->" + self.highlight.title


class CTABase(WagtailOrderable, models.Model):
    hero = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cta_hero",
        verbose_name="Hero Image",
    )

    header = models.TextField(
        blank=True,
    )

    subhead = RichTextField(
        features=base_rich_text_options,
        blank=True,
    )

    buttonTitle = models.CharField(
        verbose_name="Button Text",
        max_length=250,
        blank=True,
    )

    buttonURL = models.TextField(
        verbose_name="Button URL",
        blank=True,
    )

    panels = [
        FieldPanel("hero"),
        FieldPanel("header"),
        FieldPanel("subhead"),
        FieldPanel("buttonTitle"),
        FieldPanel("buttonURL"),
    ]

    class Meta(WagtailOrderable.Meta):
        abstract = True
        verbose_name = "cta"
        verbose_name_plural = "ctas"

    def __str__(self):
        return self.page.title + "->" + self.highlight.title


class CTA4(TranslatableMixin, CTABase):
    page = ParentalKey(
        "wagtailpages.ParticipatePage2",
        related_name="cta4",
    )


class ParticipateHighlightsBase(TranslatableMixin, WagtailOrderable, models.Model):
    page = ParentalKey(
        "wagtailpages.ParticipatePage2",
        related_name="featured_highlights",
    )
    highlight = models.ForeignKey("highlights.Highlight", on_delete=models.CASCADE, related_name="+")
    panels = [
        FieldPanel("highlight"),
    ]

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        abstract = True
        verbose_name = "highlight"
        verbose_name_plural = "highlights"

    def __str__(self):
        return self.page.title + "->" + self.highlight.title


class ParticipateHighlights(ParticipateHighlightsBase):
    page = ParentalKey(
        "wagtailpages.ParticipatePage2",
        related_name="featured_highlights",
    )


class ParticipateHighlights2(ParticipateHighlightsBase):
    page = ParentalKey(
        "wagtailpages.ParticipatePage2",
        related_name="featured_highlights2",
    )


class FocusArea(TranslatableMixin, models.Model):
    interest_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        on_delete=models.SET_NULL,
        related_name="interest_icon",
    )

    name = models.CharField(
        max_length=100,
        help_text="The name of this area of focus. Max. 100 characters.",
    )

    description = models.TextField(
        max_length=300,
        help_text="Description of this area of focus. Max. 300 characters.",
    )

    panels = [
        FieldPanel("interest_icon"),
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    translatable_fields = [
        SynchronizedField("interest_icon"),
        TranslatableField("name"),
        TranslatableField("description"),
    ]

    search_fields = [
        index.SearchField("name"),
        index.FilterField("locale_id"),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        ordering = ["name"]
        verbose_name = "Area of focus"
        verbose_name_plural = "Areas of focus"


class HomepageFocusAreas(TranslatableMixin, WagtailOrderable):
    page = ParentalKey(
        "wagtailpages.Homepage",
        related_name="focus_areas",
    )

    area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("area"),
    ]

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        verbose_name = "Homepage Focus Area"


class HomepageTakeActionCards(TranslatableMixin, WagtailOrderable):
    page = ParentalKey(
        "wagtailpages.Homepage",
        related_name="take_action_cards",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    text = models.CharField(max_length=255)
    internal_link = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    cta = models.CharField(max_length=50, default="Learn more")

    panels = [
        FieldPanel("image"),
        FieldPanel("text"),
        FieldPanel("internal_link"),
        FieldPanel("cta", heading="CTA Link Text"),
    ]

    # translatable_fields = [
    #     SynchronizedField('image'),
    #     TranslatableField('text'),
    #     SynchronizedField('internal_link'),
    # ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        verbose_name = "Take Action Card"


class PartnerLogos(TranslatableMixin, WagtailOrderable):
    page = ParentalKey(
        "wagtailpages.Homepage",
        related_name="partner_logos",
    )
    link = models.URLField(blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(
        default="Partner Name",
        blank=False,
        max_length=100,
        help_text="Alt text for the logo image.",
    )
    width = models.PositiveSmallIntegerField(
        default=100,
        help_text="The width of the image. Height will automatically be applied.",
    )
    panels = [
        FieldPanel("logo"),
        FieldPanel("name"),
        FieldPanel("link"),
        FieldPanel("width"),
    ]

    translatable_fields = [
        SynchronizedField("logo"),
        TranslatableField("name"),
        SynchronizedField("link"),
        SynchronizedField("width"),
    ]

    @property
    def image_rendition(self):
        width = self.width * 2
        return self.logo.get_rendition(f"width-{width}")

    class Meta(TranslatableMixin.Meta, WagtailOrderable.Meta):
        verbose_name = "Partner Logo"


class Homepage(FoundationMetadataPageMixin, Page):

    hero_headline = models.CharField(
        max_length=120,
        help_text="Hero story headline",
        blank=True,
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="hero_image",
    )

    def get_banner(self):
        return self.hero_image

    show_hero_button = models.BooleanField(default=True, help_text="Display hero button")

    hero_button_text = models.CharField(max_length=50, blank=True)

    hero_button_url = models.URLField(blank=True)

    hero_intro_heading = models.CharField(max_length=100, blank=True, default=hero_intro_heading_default_text)
    hero_intro_body = models.TextField(max_length=300, blank=True, default=hero_intro_body_default_text)
    hero_intro_link = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    ideas_title = models.CharField(default="Ideas", max_length=50)

    ideas_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ideas_image",
    )

    ideas_headline = models.CharField(
        max_length=140,
        blank=True,
    )

    show_cause_statement = models.BooleanField(default=False, help_text="Display cause statement")

    cause_statement = models.CharField(
        max_length=250,
        default="",
    )

    cause_statement_link_text = models.CharField(
        max_length=80,
        blank=True,
    )

    cause_statement_link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cause_statement_link",
    )

    quote_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quote_image",
    )

    quote_text = models.CharField(
        max_length=450,
        default="",
    )

    quote_source_name = models.CharField(
        max_length=100,
        default="",
    )

    quote_source_job_title = models.CharField(
        max_length=100,
        default="",
    )

    # Partner Section
    partner_heading = models.CharField(max_length=75, default="Partner with us")
    partner_intro_text = models.TextField(blank=True)
    partner_page_text = models.CharField(max_length=35, default="Let's work together")
    partner_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="partner_internal_link",
    )
    partner_background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )

    highlights_title = models.CharField(default="The Highlights", max_length=50)

    # Take Action Section
    take_action_title = models.CharField(default="Take action", max_length=50)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel(
                    "hero_headline",
                    widget=CharCountWidget(attrs={"class": "max-length-warning", "data-max-length": 120}),
                ),
                FieldPanel("show_hero_button"),
                FieldPanel("hero_button_text"),
                FieldPanel("hero_button_url"),
                FieldPanel("hero_image"),
            ],
            heading="hero",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("show_cause_statement"),
                FieldPanel("cause_statement"),
                FieldPanel("cause_statement_link_text"),
                FieldPanel("cause_statement_link_page"),
            ],
            heading="cause statement",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_intro_heading"),
                FieldPanel("hero_intro_body"),
                FieldPanel("hero_intro_link"),
            ],
            heading="Hero Intro Box",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                InlinePanel("focus_areas", min_num=3, max_num=3),
            ],
            heading="Areas of focus",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("highlights_title"),
                InlinePanel("highlights", min_num=4, max_num=4),
            ],
            heading="The Highlights",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("ideas_title"),
                FieldPanel("ideas_image"),
                FieldPanel("ideas_headline"),
                InlinePanel("ideas_posts", label="Posts", min_num=3, max_num=3),
            ],
            heading="Ideas",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("take_action_title"),
                InlinePanel("take_action_cards", label="Take Action Cards", max_num=4),
            ],
            heading="Take Action",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("quote_image"),
                FieldPanel("quote_text"),
                FieldPanel("quote_source_name"),
                FieldPanel("quote_source_job_title"),
            ],
            heading="quote",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("partner_heading"),
                FieldPanel("partner_intro_text"),
                FieldPanel("partner_page_text"),
                FieldPanel("partner_page"),
                FieldPanel("partner_background_image"),
                InlinePanel("partner_logos", label="Partner Logo", max_num=7, min_num=1),
            ],
            heading="Partner",
            classname="collapsible collapsed",
        ),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("hero_headline"),
        SynchronizedField("hero_image"),
        TranslatableField("hero_button_text"),
        SynchronizedField("hero_button_url"),
        TranslatableField("hero_intro_heading"),
        TranslatableField("hero_intro_body"),
        TranslatableField("hero_intro_link"),
        TranslatableField("ideas_title"),
        SynchronizedField("ideas_image"),
        TranslatableField("ideas_headline"),
        SynchronizedField("show_cause_statement"),
        TranslatableField("cause_statement"),
        TranslatableField("cause_statement_link_text"),
        TranslatableField("cause_statement_link_page"),
        SynchronizedField("quote_image"),
        TranslatableField("quote_text"),
        TranslatableField("quote_source_name"),
        TranslatableField("quote_source_job_title"),
        TranslatableField("partner_heading"),
        TranslatableField("partner_intro_text"),
        TranslatableField("partner_page_text"),
        SynchronizedField("partner_page"),
        SynchronizedField("partner_background_image"),
        TranslatableField("take_action_title"),
        TranslatableField("focus_areas"),
        TranslatableField("take_action_cards"),
        TranslatableField("partner_logos"),
        TranslatableField("ideas_posts"),
        TranslatableField("highlights"),
        TranslatableField("highlights_title"),
    ]

    subpage_types = [
        "AppInstallPage",
        "BanneredCampaignPage",
        "BlogIndexPage",
        "CampaignIndexPage",
        "CampaignPage",
        "MiniSiteNameSpace",
        "OpportunityPage",
        "ParticipatePage2",
        "PrimaryPage",
        "PublicationPage",
        "ResearchLandingPage",
        "RCCLandingPage",
        "Styleguide",
        "BuyersGuidePage",
        "ArticlePage",
        "donate.DonateLandingPage",
        "donate_banner.DonateBannerPage",
    ]

    def get_localized_take_action_cards(self):
        # Loop through take_action_cards and localize internal_link
        localized_cards = []
        for card in self.take_action_cards.all():
            card.internal_link = card.internal_link.localized
            localized_cards.append(card)
        return localized_cards

    def get_context(self, request):
        # We need to expose MEDIA_URL so that the s3 images will show up properly
        # due to our custom image upload approach pre-wagtail
        context = super().get_context(request)
        context["MEDIA_URL"] = settings.MEDIA_URL
        context["menu_root"] = self
        context["menu_items"] = self.get_children().live().in_menu()
        context["donate_banner"] = BasePage.get_donate_banner(self, request)
        context["localized_take_action_cards"] = self.get_localized_take_action_cards()
        if self.partner_page:
            context["localized_partner_page"] = self.partner_page.localized
        return context
