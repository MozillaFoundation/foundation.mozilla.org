from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField

from . import customblocks
from .campaigns import CampaignPage


class AppInstallPage(CampaignPage):

    zen_nav = False

    hero_heading = models.CharField(
        max_length=80,
        help_text="Hero story headline",
    )
    hero_subheading = models.CharField(
        max_length=80,
        blank=True,
        help_text="Hero story subheadline",
    )
    hero_background = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Background image for the hero section",
    )
    hero_video = models.URLField(
        null=True,
        blank=True,
        help_text="To find embed link: go to your YouTube video and click “Share,” then “Embed,” "
        "and then copy and paste the provided URL only. EX: https://www.youtube.com/embed/3FIVXBawyQ",
    )
    download_buttons = StreamField(
        [
            ("button", customblocks.AppInstallDownloadButtonBlock()),
        ],
        use_json_field=True,
        max_num=2,
    )

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("hero_heading"),
                FieldPanel("hero_subheading"),
                FieldPanel("hero_background"),
                FieldPanel("hero_video"),
                FieldPanel("download_buttons"),
            ],
            heading="Hero Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cta"),
                InlinePanel("donation_modals", label="Donation Modal", max_num=4),
                FieldPanel("body"),
            ],
            heading="Page Content",
        ),
    ]

    subpage_types = [
        "BanneredCampaignPage",
        "OpportunityPage",
    ]

    parent_page_types = ["BanneredCampaignPage", "Homepage"]
