from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.donate.models import BaseDonationPage
from networkapi.donate.pagemodels.customblocks.notice_block import NoticeBlock
from networkapi.wagtailpages.pagemodels.customblocks.base_fields import base_fields


class DonateHelpPage(BaseDonationPage):
    template = "donate/pages/help_page.html"

    parent_page_types = ["DonateLandingPage"]

    subpage_types: list = []

    max_count = 1

    notice = StreamField(
        [("notice", NoticeBlock())],
        help_text="Optional notice that will render at the top of the page.",
        blank=True,
        max_num=1,
        use_json_field=True,
    )

    body = StreamField(base_fields, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("notice"),
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
        TranslatableField("notice"),
        TranslatableField("body"),
    ]
