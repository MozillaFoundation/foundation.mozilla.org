from django.http import QueryDict
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
        TranslatableField("title"),
        TranslatableField("notice"),
        TranslatableField("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["thank_you_url"] = self.get_thank_you_url(request)
        context["show_formassembly_thank_you"] = context["request"].GET.get("thank_you") == "true"
        return context

    def get_thank_you_url(self, request):
        params = QueryDict(mutable=True)
        params.update(request.GET)
        params["thank_you"] = "true"
        return request.build_absolute_uri(request.path + "?" + params.urlencode())
