from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.search import index

from foundation_cms.core.models.home_page import HomePage
from foundation_cms.snippets.models.donate_banner import DonateBanner


class SitewideDonateBannerPage(Page):
    max_count = 1

    donate_banner = models.ForeignKey(
        DonateBanner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_donate_banner",
        help_text=(
            "CTA Banner rendered at the top of the page site-wide. "
            "Note: A/B testing of this banner will also be site-wide and across all locales."
        ),
    )

    content_panels = [
        HelpPanel(
            content=mark_safe(
                "<p>This page is where you can select a <strong>Donate Banner</strong> snippet "
                "and have it render sitewide. Feel free to name the title of this page whatever "
                "you would like, as it's just for use in the CMS only.</p>"
                "<p>To run an <strong>A/B test</strong> between two donate banners, publish this "
                "page with the banner you would like to use as 'control', then select a new donate "
                "banner that you would like to use for your variant, and click "
                "<strong>Save and Create A/B test</strong>.</p>"
                "<p><strong>Note:</strong> Please do not translate this page.</p>"
            )
        ),
        FieldPanel("title", help_text="The page title as you'd like it to be seen in the CMS."),
        MultiFieldPanel(
            [
                FieldPanel("donate_banner"),
            ],
            heading="Donate Banner",
            classname="collapsible",
        ),
    ]

    search_fields = Page.search_fields + [
        index.RelatedFields(
            "donate_banner",
            [
                index.SearchField("name", boost=6),
                index.SearchField("title", boost=6),
                index.SearchField("subtitle", boost=5),
                index.SearchField("cta_button_text", boost=4),
            ],
        ),
        index.FilterField("id"),
        index.FilterField("locale_id"),
    ]

    promote_panels: list = []

    subpage_types: list = []

    parent_page_types = [HomePage]

    template = "patterns/components/previews/donate_banner.html"

    class Meta:
        verbose_name = "Donate Banner Page"
        verbose_name_plural = "Donate Banner Pages"

    # Override the context for template purposes
    def get_context(self, request):
        context = super().get_context(request)
        context["object"] = self.donate_banner
        return context


@receiver(post_delete, sender=SitewideDonateBannerPage)
def delete_all_donate_banner_page_translations(sender, instance, **kwargs):
    """
    Deletes all translated instances of the SitewideDonateBannerPage, as they don't auto-delete.
    This prevents lingering aliases from blocking the creation of a new SitewideDonateBannerPage
    due to the max_count=1 limit.
    """
    SitewideDonateBannerPage.objects.all().delete()
