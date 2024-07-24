import json

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels import customblocks
from networkapi.wagtailpages.pagemodels.base import BasePage

from ..customblocks.full_content_rich_text_options import full_content_rich_text_options


class BuyersGuideCampaignPageDonationModalRelation(TranslatableMixin, Orderable):
    page = ParentalKey(
        "BuyersGuideCampaignPage",
        related_name="donation_modal_relations",
    )
    donation_modal = models.ForeignKey(
        "DonationModal",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text="Choose existing or create new donation modal",
    )

    panels = [
        FieldPanel("donation_modal"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class BuyersGuideCampaignPage(BasePage):
    parent_page_types = ["BuyersGuideEditorialContentIndexPage"]
    subpage_types: list = []
    template = "pages/buyersguide/campaign_page.html"

    cta = models.ForeignKey(
        "CTA",
        related_name="buyersguide_campaign_page_for_cta",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose one of our call-to-action snippets, or create a new one.",
    )
    header = models.CharField(max_length=250, blank=True)
    narrowed_page_content = models.BooleanField(
        default=False,
        help_text="For text-heavy pages, turn this on to reduce the overall width of the content on the page.",
    )
    body = StreamField(
        block_types=(
            ("accordion", customblocks.AccordionBlock()),
            (
                "paragraph",
                RichTextBlock(
                    features=full_content_rich_text_options,
                    template="wagtailpages/blocks/rich_text_block.html",
                ),
            ),
            ("card_grid", customblocks.CardGridBlock()),
            ("image_grid", customblocks.ImageGridBlock()),
            ("iframe", customblocks.iFrameBlock()),
            ("image", customblocks.AnnotatedImageBlock()),
            ("audio", customblocks.AudioBlock()),
            ("image_text", customblocks.ImageTextBlock()),
            ("image_text_mini", customblocks.ImageTextMini()),
            ("video", customblocks.VideoBlock()),
            ("linkbutton", customblocks.LinkButtonBlock()),
            ("looping_video", customblocks.LoopingVideoBlock()),
            ("pulse_listing", customblocks.PulseProjectList()),
            ("single_quote", customblocks.SingleQuoteBlock()),
            ("slider", customblocks.FoundationSliderBlock()),
            ("spacer", customblocks.BootstrapSpacerBlock()),
            ("airtable", customblocks.AirTableBlock()),
            ("datawrapper", customblocks.DatawrapperBlock()),
            ("typeform", customblocks.TypeformBlock()),
        ),
        use_json_field=True,
    )

    def get_donation_modal_json(self):
        modals = self.donation_modal_relations.all()
        modals_json = [m.donation_modal.to_simple_dict() for m in modals]
        return json.dumps(modals_json)

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("cta"),
        MultipleChooserPanel(
            "donation_modal_relations", label="Donation Modal", chooser_field_name="donation_modal", max_num=4
        ),
        FieldPanel("body"),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("narrowed_page_content"),
            ],
            classname="collapsible",
        ),
    ]

    translatable_fields = [
        # Content tab fields
        # FIXME: Contingency fix while https://github.com/mozilla/foundation.mozilla.org/pull/7771 is sorted out
        # TranslatableField('cta'),
        TranslatableField("title"),
        TranslatableField("header"),
        SynchronizedField("narrowed_page_content"),
        TranslatableField("body"),
        TranslatableField("donation_modal_relations"),
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]
