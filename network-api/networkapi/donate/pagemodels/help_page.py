from urllib.parse import urlencode

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.donate.models import BaseDonationPage
from networkapi.donate.snippets.help_page_notice import HelpPageNotice
from networkapi.wagtailpages.pagemodels.customblocks.base_fields import base_fields


class DonateHelpPage(BaseDonationPage):
    template = "donate/pages/help_page.html"

    parent_page_types = ["DonateLandingPage"]

    subpage_types: list = []

    max_count = 1

    notice = models.ForeignKey(
        HelpPageNotice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Optional notice that will render at the top of the page.",
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
        TranslatableField("title"),
        SynchronizedField("notice"),
        TranslatableField("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["localized_notice"] = self.get_localized_notice()
        context["thank_you_url"] = self.get_thank_you_url(request)
        context["show_formassembly_thank_you"] = context["request"].GET.get("thank_you") == "true"
        return context

    def get_localized_notice(self):
        """Returns the localized notice if it exists, otherwise None."""
        if self.notice:
            return self.notice.localized
        return None

    def get_thank_you_url(self, request):
        base_url = self.get_full_url()
        existing_params = request.GET.dict()
        existing_params["thank_you"] = "true"
        thank_you_url = base_url + "?" + urlencode(existing_params)
        return thank_you_url
