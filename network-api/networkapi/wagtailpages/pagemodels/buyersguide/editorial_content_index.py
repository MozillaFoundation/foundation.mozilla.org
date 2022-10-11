from typing import TYPE_CHECKING, Optional

from django import shortcuts
from django.core import paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel, MultiFieldPanel
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
    subpage_types = ['wagtailpages.BuyersGuideArticlePage']
    template = 'pages/buyersguide/editorial_content_index_page.html'

    content_panels = wagtail_models.Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel(
                    'related_article_relations',
                    heading='Related articles',
                    label='Article',
                    max_num=3,
                ),
            ],
            heading='Related Articles',
        ),
    ]

    items_per_page: int = 10

    @routable_models.route('items/', name='items')
    def items_route(self, request: 'http.HttpRequest') -> 'http.HttpResponse':
        items = self.get_paginated_items(page=request.GET.get('page'))
        return shortcuts.render(
            request=request,
            template_name='fragments/buyersguide/editorial_content_index_items.html',
            context={'items': items},
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["featured_cta"] = get_buyersguide_featured_cta(self)
        context["items"] = self.get_paginated_items(request.GET.get('page'))
        return context

    def get_paginated_items(
        self,
        page: Optional[int] = None
    ) -> 'paginator.Page[pagemodels.BuyersGuideArticlePage]':
        """Get a page of items to list in the index."""
        items = self.get_items()
        items_paginator = paginator.Paginator(
            object_list=items,
            per_page=self.items_per_page,
        )
        return items_paginator.get_page(page)

    def get_items(self) -> 'models.QuerySet[pagemodels.BuyersGuideArticlePage]':
        """Get items to list in the index."""
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
