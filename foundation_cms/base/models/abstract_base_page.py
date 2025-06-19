from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataPageMixin

from foundation_cms.blocks import (
    AudioBlock,
    CustomImageBlock,
    ImpactNumberBlock,
    LinkButtonBlock,
    ListBlock,
    NewsletterSignupBlock,
    PortraitCardSetBlock,
    QuoteBlock,
    SpacerBlock,
    TabbedContentContainerBlock,
    TimelyActivationsCardsBlock,
    TwoColumnContainerBlock,
    VideoBlock,
)

# Shared StreamField block types for use across pages that inherit from AbstractBasePage.
# Extend this list in specific page models (e.g., HomePage) to add more blocks as needed.
base_page_block_options = [
    ("rich_text", RichTextBlock()),
    ("image", CustomImageBlock()),
    ("audio_block", AudioBlock()),
    ("tabbed_content", TabbedContentContainerBlock()),
    ("two_column_container_block", TwoColumnContainerBlock()),
    ("link_button_block", LinkButtonBlock()),
    ("portrait_card_set_block", PortraitCardSetBlock()),
    ("spacer_block", SpacerBlock()),
    ("impact_numbers", ImpactNumberBlock()),
    ("newsletter_signup", NewsletterSignupBlock()),
    ("timely_activations_cards", TimelyActivationsCardsBlock()),
    ("quote", QuoteBlock()),
    ("list_block", ListBlock()),
    ("video_block", VideoBlock()),
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


class AbstractBasePage(MetadataPageMixin, Page):
    theme = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[("default", "Default"), ("magazine", "Magazine")],
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

    promote_panels = Page.promote_panels + [
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
        if self.theme:
            return self.theme

        # Traverse ancestors to find a page with an explicitly set theme
        for ancestor in reversed(self.get_ancestors(inclusive=False).live()):
            if hasattr(ancestor, "theme") and ancestor.theme:
                return ancestor.theme

        return "default"


class TaggedPage(ItemBase):
    tag = models.ForeignKey(PageTag, related_name="tagged_pages", on_delete=models.CASCADE)
    content_object = ParentalKey(to="wagtailcore.Page", on_delete=models.CASCADE, related_name="base_tagged_items")
