from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.customblocks import LinkBlock
from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)


class BuyersGuideCallToAction(index.Indexed, TranslatableMixin, models.Model):
    """
    Reusable call to action for the buyers guide,
    features a title and rich text content, with optional image and link.
    """

    sticker_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Sticker Image",
        help_text="Optional image on CTA.",
    )
    title = models.CharField(max_length=200)
    content = RichTextField(features=base_rich_text_options, blank=True)
    link = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    panels = [
        FieldPanel("sticker_image"),
        FieldPanel("title"),
        FieldPanel("content"),
        MultiFieldPanel(
            [
                FieldPanel("link"),
            ],
            heading="Call To Action Link",
        ),
    ]

    translatable_fields = [
        SynchronizedField("sticker_image"),
        TranslatableField("title"),
        TranslatableField("content"),
        TranslatableField("link"),
    ]

    search_fields = [
        index.SearchField("title", boost=10),
        index.AutocompleteField("title", boost=10),
        index.SearchField("link_label"),
        index.FilterField("locale_id"),
    ]

    class Meta(TranslatableMixin.Meta):
        ordering = ["title"]
        verbose_name = "Buyers Guide Call To Action"
        verbose_name_plural = "Buyers Guide Call To Actions"

    def __str__(self):
        return self.title

    def link_label(self):
        if self.link:
            link_block = self.link[0]
            return link_block.value["label"]
        return ""

    def link_url(self):
        if self.link:
            link_block = self.link[0]
            return link_block.value.url
        return ""
