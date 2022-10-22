from typing import TYPE_CHECKING, Optional

from django import shortcuts
from django.core import paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel
from wagtail.core import models as wagtail_models
from wagtail.core.models import Orderable, TranslatableMixin
from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages.pagemodels.buyersguide.utils import get_buyersguide_featured_cta
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
    parent_page_types = ['wagtailpages.BuyersGuidePage']
    subpage_types = [
        'wagtailpages.BuyersGuideArticlePage',
        'wagtailpages.BuyersGuideCampaignPage',
        ]
    template = 'pages/buyersguide/editorial_content_index_page.html'

    content_panels = wagtail_models.Page.content_panels + [
        InlinePanel(
            'related_article_relations',
            heading='Popular articles',
            label='Article',
            max_num=3,
        ),
    ]

    items_per_page: int = 10

    def serve(self, request: 'http.HttpRequest', *args, **kwargs) -> 'http.HttpResponse':
        if request.htmx:
            # This is an HTMX request and we are only interested in the items list.
            items = self.get_items()
            paginated_items = self.paginate_items(
                items=items,
                page=request.GET.get('page'),
            )
            return self.render_items(request=request, items=paginated_items)
        return super().serve(request, *args, **kwargs)

    @routable_models.route(r'^press/$', name='press')
    def press_route(self, request: 'http.HttpRequest') -> 'http.HttpResponse':
        return None

    def render_items(
        self,
        request: 'http.HttpRequest',
        items: 'models.QuerySet[pagemodels.BuyersGuideArticlePage]',
    ) -> 'http.HttpResponse':
        '''
        Method to return only the content index items.

        This method does not return a full page, but only an HTML fragment of list
        items that is meant to be requested with AJAX and used to extend an existing
        list of items.

        '''
        return shortcuts.render(
            request=request,
            template_name='fragments/buyersguide/editorial_content_index_items.html',
            context={
                'index_page': self,
                'items': items,
                'show_load_more_button_immediately': True,
            },
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["featured_cta"] = get_buyersguide_featured_cta(self)
        items = self.get_items()
        context["items"] = self.paginate_items(
            items=items,
            page=request.GET.get('page'),
        )
        return context

    def paginate_items(
        self,
        items: 'models.QuerySet[pagemodels.BuyersGuideArticlePage]',
        page: 'Optional[int]' = None,
    ) -> 'paginator.Page[pagemodels.BuyersGuideArticlePage]':
        """Pagingate the given items."""
        items_paginator = paginator.Paginator(
            object_list=items,
            per_page=self.items_per_page,
        )
        return items_paginator.get_page(page)

    def get_items(self) -> 'models.QuerySet[pagemodels.BuyersGuideArticlePage]':
        """Get default items to list in the index."""
        return (
            self.get_descendants()
            .order_by("-first_published_at")
            .public()
            .live()
            .specific()
        )

    def get_related_articles(self) -> list['pagemodels.BuyersGuideArticlePage']:
        return orderables.get_related_items(
            self.related_article_relations.all(),
            'article',
        )


class BuyersGuideEditorialContentIndexPageArticlePageRelation(TranslatableMixin, Orderable):
    page = ParentalKey(
        'wagtailpages.BuyersGuideEditorialContentIndexPage',
        related_name='related_article_relations',
    )
    article = models.ForeignKey(
        'wagtailpages.BuyersGuideArticlePage',
        on_delete=wagtail_models.models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [PageChooserPanel('article')]

    def __str__(self):
        return f'{self.category.name} -> {self.article.title}'

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass
