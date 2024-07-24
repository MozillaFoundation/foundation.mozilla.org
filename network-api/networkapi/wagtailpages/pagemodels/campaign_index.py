from django.db import models
from modelcluster import fields as cluster_fields
from wagtail.admin.panels import MultipleChooserPanel, PageChooserPanel
from wagtail.models import Orderable, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from .index import IndexPage


class FeaturedCampaignPageRelation(TranslatableMixin, Orderable):
    index_page = cluster_fields.ParentalKey(
        "wagtailpages.CampaignIndexPage",
        related_name="featured_campaign_pages",
    )
    featured_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [PageChooserPanel("featured_page", ["wagtailpages.BanneredCampaignPage", "wagtailpages.CampaignPage"])]

    def __str__(self):
        return f"{self.index_page.title} -> {self.featured_page.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class CampaignIndexPage(IndexPage):
    """
    The campaign index is specifically for campaign-related pages
    """

    subpage_types = [
        "BanneredCampaignPage",
        "CampaignPage",
        "DearInternetPage",
        "OpportunityPage",
        "YoutubeRegretsPage",
        "YoutubeRegretsReporterPage",
        "PublicationPage",
        "ArticlePage",
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields from IndexPage
        TranslatableField("title"),
        TranslatableField("intro"),
        TranslatableField("header"),
        SynchronizedField("page_size"),
        SynchronizedField("featured_campaign_pages"),
    ]

    template = "wagtailpages/index_page.html"

    content_panels = IndexPage.content_panels + [
        MultipleChooserPanel(
            "featured_campaign_pages",
            label="Featured Pages",
            chooser_field_name="featured_page",
        ),
    ]

    def get_entries(self, context=None):
        """
        Fetches the featured pages related to this index page ordered by their 'sort_order',
        and returns them as their specific page instances.
        """
        relations = self.featured_campaign_pages.all().order_by("sort_order")
        featured_pages = [relation.featured_page.specific for relation in relations]
        return featured_pages

    def get_context(self, request):
        # bootstrap the render context
        context = super().get_context(request)
        entries = self.get_entries()
        context["entries"] = entries[0 : self.page_size]
        return context
