from django.db import models
from django.template.loader import select_template
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

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
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="author_image"
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
class PageTag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "Page Tag (new)"
        verbose_name_plural = "Page Tags (new)"


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
    tags = ClusterTaggableManager(through="base.TaggedPage", blank=True)
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
                FieldPanel("tags"),
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
        return context


class TaggedPage(ItemBase):
    tag = models.ForeignKey(PageTag, related_name="tagged_pages", on_delete=models.CASCADE)
    content_object = ParentalKey(to="wagtailcore.Page", on_delete=models.CASCADE, related_name="base_tagged_items")
