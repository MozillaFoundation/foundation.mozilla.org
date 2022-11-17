from typing import TYPE_CHECKING, Optional

from django import shortcuts
from django.core import paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel
from wagtail.core import models as wagtail_models
from wagtail.core.models import Orderable, TranslatableMixin
from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages.pagemodels.buyersguide.utils import (
    get_categories_for_locale,
    get_buyersguide_featured_cta,
)
from networkapi.wagtailpages.utils import get_language_from_request
from networkapi.utility import orderables
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata

if TYPE_CHECKING:
    from django import http
    from networkapi.wagtailpages import models as pagemodels


class BuyersGuideEditorialContentIndexPage(
    foundation_metadata.FoundationMetadataPageMixin,
    routable_models.RoutablePageMixin,
    wagtail_models.Page,
):
    parent_page_types = ["wagtailpages.BuyersGuidePage"]
    subpage_types = [
        "wagtailpages.BuyersGuideArticlePage",
        "wagtailpages.BuyersGuideCampaignPage",
    ]
    template = "pages/buyersguide/editorial_content_index_page.html"

    content_panels = wagtail_models.Page.content_panels + [
        InlinePanel(
            "related_article_relations",
            heading="Popular articles",
            label="Article",
            max_num=3,
        ),
    ]

    items_per_page: int = 10

    def serve(self, request: "http.HttpRequest", *args, **kwargs) -> "http.HttpResponse":
        if request.htmx:
            # This is an HTMX request and we are only interested in the items list.
            items = self.get_items()
            paginated_items = self.paginate_items(
                items=items,
                page=request.GET.get("page"),
            )
            return self.render_items(request=request, items=paginated_items)
        return super().serve(request, *args, **kwargs)

    def render_items(
        self,
        request: "http.HttpRequest",
        items: "models.QuerySet[pagemodels.BuyersGuideArticlePage]",
    ) -> "http.HttpResponse":
        """
        Method to return only the content index items.

        This method does not return a full page, but only an HTML fragment of list
        items that is meant to be requested with AJAX and used to extend an existing
        list of items.

        Because this method is only meant for AJAX requests, we can also assume that JS works
        and thus show the 'load more' button immediately.

        """
        return shortcuts.render(
            request=request,
            template_name="fragments/buyersguide/editorial_content_index_items.html",
            context={
                "index_page": self,
                "items": items,
                "show_load_more_button_immediately": True,
            },
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["featured_cta"] = get_buyersguide_featured_cta(self)

        language_code = get_language_from_request(request)
        context["categories"] = get_categories_for_locale(language_code)

        items = self.get_items()
        context["items"] = self.paginate_items(
            items=items,
            page=request.GET.get("page"),
            expanded=request.GET.get("expanded", "false") == "true",
        )
        return context

    def paginate_items(
        self,
        items: "models.QuerySet[pagemodels.BuyersGuideArticlePage]",
        page: "Optional[str]" = None,
        expanded: bool = False,
    ) -> "paginator.Page[pagemodels.BuyersGuideArticlePage]":
        """
        Pagingate the given items.

        Return only the requested page of items. The number of items per page is
        defined by `self.items_per_page`.

        The page can be expanded. This means the page will include the items from
        all previous pages as well. It does not include items from following pages.

        """
        items_paginator = paginator.Paginator(
            object_list=items,
            per_page=self.items_per_page,
        )
        page_of_items = items_paginator.get_page(page)
        if not expanded:
            return page_of_items

        # Override the object_list on the page with the full object list, but trimmed to the last index
        # that the page would display.
        index_of_last_item_on_page = page_of_items.end_index()
        page_of_items.object_list = items_paginator.object_list[:index_of_last_item_on_page]
        # The page is expanded, so there should be no previous page. All items are already on the page.
        page_of_items.has_previous = lambda: False

        return page_of_items

    def get_items(self) -> "models.QuerySet[pagemodels.BuyersGuideArticlePage]":
        """Get items to list in the index."""
        return self.get_descendants().order_by("-first_published_at").public().live().specific()

    def get_related_articles(self) -> list["pagemodels.BuyersGuideArticlePage"]:
        return orderables.get_related_items(
            self.related_article_relations.all(),
            "article",
        )


class BuyersGuideEditorialContentIndexPageArticlePageRelation(TranslatableMixin, Orderable):
    page = ParentalKey(
        "wagtailpages.BuyersGuideEditorialContentIndexPage",
        related_name="related_article_relations",
    )
    article = models.ForeignKey(
        "wagtailpages.BuyersGuideArticlePage",
        on_delete=wagtail_models.models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [PageChooserPanel("article")]

    def __str__(self):
        return f"{self.category.name} -> {self.article.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass
