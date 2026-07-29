from django.db import models
from wagtail.admin.panels import FieldPanel, HelpPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import PreviewableMixin, TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.blocks.link_button_block import LinkButtonBlock
from foundation_cms.constants import NOTICE_BANNER_RICH_TEXT_FEATURES


@register_snippet
class NoticeBanner(TranslatableMixin, PreviewableMixin, models.Model):
    """
    A reusable, page-level notice strip for temporary or contextual messaging
    (deprecation notices, redirects, sunset announcements, general alerts).

    Editors select one of these on the Promote tab of a page; see
    `AbstractBasePage.notice_banner` and `BasePage.notice_banner`.
    """

    name = models.CharField(
        max_length=100,
        help_text="Identify this notice for editors. This is not displayed on the banner.",
    )
    body = RichTextField(
        features=NOTICE_BANNER_RICH_TEXT_FEATURES,
        help_text=(
            "The notice message. Headings are limited to Heading 4-6 so the notice "
            "does not compete with the page's own headings."
        ),
    )
    cta = StreamField(
        [("link_button", LinkButtonBlock())],
        blank=True,
        max_num=1,
        help_text="Optional call to action button.",
    )

    panels = [
        HelpPanel(
            content=(
                "To show this notice on a page, edit that page and choose it under "
                "&ldquo;Notice banner&rdquo; on the Promote tab."
            )
        ),
        FieldPanel("name"),
        FieldPanel("body"),
        FieldPanel("cta"),
    ]

    translatable_fields = [
        SynchronizedField("name"),
        TranslatableField("body"),
        TranslatableField("cta"),
    ]

    search_fields = [
        index.SearchField("name"),
        index.SearchField("body"),
        index.FilterField("locale_id"),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Notice Banner"
        verbose_name_plural = "Notice Banners"

    def __str__(self):
        return self.name

    def get_preview_template(self, request, mode_name):
        return "patterns/components/previews/notice_banner.html"
