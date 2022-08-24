from wagtail.core import models as wagtail_models
from modelcluster.fields import ParentalKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import PageChooserPanel, InlinePanel, MultiFieldPanel, FieldPanel
from wagtail.core.models import Orderable, TranslatableMixin
from networkapi.wagtailpages.pagemodels import orderables

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


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

    objects = orderables.OrderableRelationQuerySet.as_manager()
    related_item_field_name = "article"

    def __str__(self):
        return f'{self.category.name} -> {self.article.title}'

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class BuyersGuideEditorialContentIndexPage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    parent_page_types = ['wagtailpages.BuyersGuidePage']
    subpage_types = ['wagtailpages.BuyersGuideArticlePage']
    template = 'pages/buyersguide/editorial_content_index_page.html'

    related_articles_heading = models.CharField(
        max_length=50,
        default=_('Related'),
        blank=False,
        null=False,
        help_text=(
            'Heading for the related/featured articles section.'
            'Common choices are "Related", "Popular", etc.'
        ),
    )

    content_panels = wagtail_models.Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('related_articles_heading', heading='Heading'),
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
        context["items"] = self.get_descendants().public().live()
        return context
