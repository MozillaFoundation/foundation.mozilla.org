import typing

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.core import models as wagtail_models
from wagtail.core.models import Orderable, TranslatableMixin
from networkapi.wagtailpages.pagemodels.buyersguide.utils import get_featured_cta

from networkapi.utility import orderables
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


if typing.TYPE_CHECKING:
    from networkapi.wagtailpages.models import BuyersGuideArticlePage


class BuyersGuideEditorialContentIndexPage(
    foundation_metadata.FoundationMetadataPageMixin,
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["featured_cta"] = get_featured_cta(self)
        context["items"] = self.get_descendants().public().live()
        return context

    def get_related_articles(self) -> list['BuyersGuideArticlePage']:
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
