from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.utils import CharCountWidget

from .campaigns import CampaignPage
from .customblocks.app_install_download_button_block import (
    AppInstallDownloadButtonBlock,
)
from wagtail.images import get_image_model_string


class AppInstallPage(CampaignPage):

    hero_heading = models.CharField(
        max_length=250,
        help_text="Hero story headline",
    )
    hero_subheading = models.CharField(
        max_length=250,
        blank=True,
        help_text="Hero story subheadline",
    )
    hero_background = models.ForeignKey(
        get_image_model_string(),
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
            ("button", AppInstallDownloadButtonBlock()),
        ],
        use_json_field=True,
        max_num=2,
        blank=True,
    )

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("hero_background"),
                FieldPanel(
                    "hero_heading",
                    classname="full title",
                    widget=CharCountWidget(attrs={"class": "max-length-warning", "data-max-length": 80}),
                ),
                FieldPanel(
                    "hero_subheading",
                    classname="full title",
                    widget=CharCountWidget(attrs={"class": "max-length-warning", "data-max-length": 80}),
                ),
                FieldPanel("download_buttons"),
                FieldPanel("hero_video"),
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

    translatable_fields = CampaignPage.translatable_fields + [
        SynchronizedField("hero_background"),
        TranslatableField("hero_heading"),
        TranslatableField("hero_subheading"),
        TranslatableField("download_buttons"),
        SynchronizedField("hero_video"),
    ]

    subpage_types = [
        "BanneredCampaignPage",
        "OpportunityPage",
    ]

    parent_page_types = ["BanneredCampaignPage", "Homepage"]
