import re

from django.apps import apps
from django.db import models
from django.template.loader import select_template
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Locale, Page
from wagtail.snippets.models import register_snippet
from wagtail_ab_testing.models import AbTest

from foundation_cms.blocks import (
    AudioBlock,
    CustomImageBlock,
    DividerBlock,
    FeaturedCardBlock,
    ImpactNumberBlock,
    LinkButtonBlock,
    ListBlock,
    NewsletterSignupBlock,
    PillarCardSetBlock,
    PortraitCardSetBlock,
    QuoteBlock,
    SpacerBlock,
    SpotlightCardSetBlock,
    TabbedContentContainerBlock,
    TimelyActivationsCardsBlock,
    TitleBlock,
    TwoColumnContainerBlock,
    VideoBlock,
    iFrameBlock,
)
from foundation_cms.mixins.foundation_metadata import FoundationMetadataPageMixin

# Shared StreamField block types for use across pages that inherit from AbstractBasePage.
# Extend this list in specific page models (e.g., HomePage) to add more blocks as needed.
base_page_block_options = [
    # [TODO/FIXME] consider ordering or grouping these blocks
    (
        "rich_text",
        RichTextBlock(
            template="patterns/blocks/themes/default/rich_text_block.html",
        ),
    ),
    ("image", CustomImageBlock()),
    ("audio_block", AudioBlock()),
    ("tabbed_content", TabbedContentContainerBlock()),
    ("two_column_container_block", TwoColumnContainerBlock()),
    ("link_button_block", LinkButtonBlock()),
    ("portrait_card_set_block", PortraitCardSetBlock()),
    ("spotlight_card_set_block", SpotlightCardSetBlock()),
    ("spacer_block", SpacerBlock()),
    ("iframe_block", iFrameBlock()),
    ("impact_numbers", ImpactNumberBlock()),
    ("newsletter_signup", NewsletterSignupBlock()),
    ("timely_activations_cards", TimelyActivationsCardsBlock()),
    ("quote", QuoteBlock()),
    ("list_block", ListBlock()),
    ("video_block", VideoBlock()),
    ("pillar_card_set", PillarCardSetBlock()),
    ("featured_card_block", FeaturedCardBlock()),
    ("divider", DividerBlock()),
    ("title_block", TitleBlock()),
]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Author image",
    )
    bio = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("bio"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


@register_snippet
class Topic(TagBase):
    free_tagging = False
    description = models.TextField(blank=True, help_text="Optional description shown on topic listing page.")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Page Topic (new)"
        verbose_name_plural = "Page Topics (new)"

    # TODO:FIXME Topic listing route should not live under the NP tree
    def get_topic_listing_url(self):
        """Get the Nothing Personal listing URL for this topic"""
        from foundation_cms.nothing_personal.models import NothingPersonalHomePage

        np_home = NothingPersonalHomePage.objects.live().first()
        if np_home:
            return f"{np_home.url}topics/{self.slug}/"
        return None


class AbstractBasePage(FoundationMetadataPageMixin, Page):
    theme = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[("default", "Default"), ("nothing_personal", "Nothing Personal")],
        help_text="Optional. If unset, theme will be inherited from section root.",
    )
    body = StreamField(
        base_page_block_options,
        use_json_field=True,
        blank=True,
    )
    topics = ClusterTaggableManager(
        through="base.PageTopic",
        blank=True,
        verbose_name="Page Topics",
        help_text="Add one or more topics. Start typing to search, then press Enter.",
    )
    author = models.ForeignKey(
        "base.Author",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_pages",
    )

    promote_panels = FoundationMetadataPageMixin.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("topics"),
            ],
            heading="Additional Metadata",
        )
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("theme"),
    ]

    class Meta:
        abstract = True

    def get_theme(self):
        # per-instance memoize for this render
        if hasattr(self, "_resolved_theme"):
            return self._resolved_theme

        # return if theme is explicitly set on this page
        if self.theme:
            self._resolved_theme = self.theme
            return self._resolved_theme

        # walk up nearest-first ancestor to try to find a theme
        ancestors = self.get_ancestors(inclusive=False).select_related("content_type").defer_streamfields()

        for ancestor in reversed(ancestors):
            sp = ancestor.specific
            if isinstance(sp, AbstractBasePage):
                theme = getattr(sp, "theme", None)
                if theme:
                    self._resolved_theme = theme
                    return theme

        # default theme is fallback
        self._resolved_theme = "default"
        return self._resolved_theme

    def themed_template_names(self, base_template: str) -> list[str]:
        """
        Build a ordered list of page templates. Order matters since wagtail will render the first one it finds.
        `base_template` can be a full default path (e.g. "patterns/pages/core/general_page.html")
        or just a filename (e.g. "general_page.html").
        """
        filename = base_template.rsplit("/", 1)[-1]
        theme = self.get_theme()

        return [
            f"patterns/pages/themes/{theme}/{filename}",
            (base_template if "/" in base_template else f"patterns/pages/core/{filename}"),
        ]

    def get_template(self, request, *args, **kwargs):
        return self.themed_template_names(self.template)

    def get_preview_template(self, request, mode_name):
        return self.get_template(request)

    def get_donate_banner(self, request):
        SitewideDonateBannerPage = apps.get_model("core", "SitewideDonateBannerPage")

        # Check if there's a SitewideDonateBannerPage.
        default_locale = Locale.get_default()
        donate_banner_page = SitewideDonateBannerPage.objects.filter(locale=default_locale).first()
        # If there is no SitewideDonateBannerPage or no donate_banner is set, return None.
        if not donate_banner_page or not donate_banner_page.donate_banner:
            return None

        # Check if the user has Do Not Track enabled by inspecting the DNT header.
        dnt_enabled = request.headers.get("DNT") == "1"

        # Check if there's an active A/B test for the SitewideDonateBannerPage.
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
        theme = self.get_theme()
        context["theme"] = theme
        context["theme_base"] = select_template(
            [
                f"base/themes/{theme}/base.html",
                "base/base.html",
            ]
        ).template.name
        context["donate_banner"] = self.get_donate_banner(request)
        context["page_type_bem"] = self._to_bem_case(self.specific_class.__name__)
        context["theme_class_bem"] = self._to_bem_case(theme) if theme else ""
        return context

    def _to_bem_case(self, name):
        """Convert CamelCase to kebab-case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
        """ Replace underscore with just dash """
        s1 = s1.replace("_", "-")
        return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


class PageTopic(TaggedItemBase):
    """
    Through model connecting a Page to a Topic.
    """

    # must be named 'tag' for django-taggit to work.
    tag = models.ForeignKey(Topic, related_name="page_relations", on_delete=models.CASCADE)
    content_object = ParentalKey(to="wagtailcore.Page", on_delete=models.CASCADE, related_name="topic_relations")
