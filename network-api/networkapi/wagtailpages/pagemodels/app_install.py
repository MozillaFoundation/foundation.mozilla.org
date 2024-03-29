from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

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
    button1_text = models.CharField(
        max_length=50,
        help_text="Text for Button 1",
        null=True,
        blank=True,
    )
    button1_download_link = models.URLField(
        max_length=255,
        help_text="Download link for Button 1",
        null=True,
        blank=True,
    )
    button1_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image for Button 1",
    )
    button2_text = models.CharField(
        max_length=50,
        help_text="Text for Button 2",
        null=True,
        blank=True,
    )
    button2_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image for Button 2",
    )
    button2_download_link = models.URLField(
        max_length=255,
        help_text="Download link for Button 2",
        null=True,
        blank=True,
    )

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("hero_heading"),
                FieldPanel("hero_subheading"),
                FieldPanel("hero_background"),
                FieldPanel("hero_video"),
                MultiFieldPanel(
                    [
                        FieldPanel("button1_image"),
                        FieldPanel("button1_text"),
                        FieldPanel("button1_download_link"),
                        FieldPanel("button2_image"),
                        FieldPanel("button2_text"),
                        FieldPanel("button2_download_link"),
                    ],
                    heading="Download Link Buttons",
                ),
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
