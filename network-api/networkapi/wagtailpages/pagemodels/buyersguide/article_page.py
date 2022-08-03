from django import http
from django.db import models
from modelcluster import fields as cluster_fields
from wagtail import images
from wagtail.admin import edit_handlers as panels
from wagtail.core import blocks, fields
from wagtail.core import models as wagtail_models
from wagtail.images import edit_handlers as image_panels
from wagtail.snippets import edit_handlers as snippet_panels

from networkapi.wagtailpages.pagemodels import customblocks
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class BuyersGuideArticlePage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page
):
    parent_page_types = ['wagtailpages.BuyersGuideEditorialContentIndexPage']
    subpage_types: list = []
    template = 'pages/buyersguide/article_page.html'

    hero_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Image for the hero section of the page.',
    )
    body = fields.StreamField(
        block_types=(
            ('accordion', customblocks.AccordionBlock()),
            ('paragraph', blocks.RichTextBlock(
                features=customblocks.full_content_rich_text_options,
                template='wagtailpages/blocks/rich_text_block.html',
            )),
            ('card_grid', customblocks.CardGridBlock()),
            ('image_grid', customblocks.ImageGridBlock()),
            ('iframe', customblocks.iFrameBlock()),
            ('image', customblocks.AnnotatedImageBlock()),
            ('audio', customblocks.AudioBlock()),
            ('image_text', customblocks.ImageTextBlock()),
            ('image_text_mini', customblocks.ImageTextMini()),
            ('video', customblocks.VideoBlock()),
            ('linkbutton', customblocks.LinkButtonBlock()),
            ('looping_video', customblocks.LoopingVideoBlock()),
            ('pulse_listing', customblocks.PulseProjectList()),
            ('single_quote', customblocks.SingleQuoteBlock()),
            ('slider', customblocks.FoundationSliderBlock()),
            ('spacer', customblocks.BootstrapSpacerBlock()),
            ('airtable', customblocks.AirTableBlock()),
            ('datawrapper', customblocks.DatawrapperBlock()),
            ('typeform', customblocks.TypeformBlock()),
        ),
        block_counts={'typeform': {'max_num': 1}},
        null=True,
        blank=False,
    )

    content_panels = wagtail_models.Page.content_panels + [
        image_panels.ImageChooserPanel('hero_image'),
        panels.InlinePanel('author_profile_relations', heading='Authors', label='Author'),
        panels.InlinePanel(
            'content_category_relations',
            heading='Content categories',
            label='Content category',
            max_num=2,
        ),
        panels.InlinePanel(
            'related_article_relations',
            heading='Related articles',
            label='Article',
            max_num=6,
        ),
        panels.StreamFieldPanel('body'),
    ]

    def get_context(self, request: http.HttpRequest, *args, **kwargs) -> dict:
        context = super().get_context(request, *args, **kwargs)
        context['home_page'] = self.get_parent().get_parent().specific
        return context

    def get_related_articles(self) -> models.QuerySet['BuyersGuideArticlePage']:
        related_article_ids = self.related_article_relations.values_list(
            'article_id',
            flat=True,
        )
        return BuyersGuideArticlePage.objects.filter(id__in=related_article_ids)

    def get_primary_related_articles(self) -> models.QuerySet['BuyersGuideArticlePage']:
        return self.get_related_articles()[:3]

    def get_secondary_related_articles(self) -> models.QuerySet['BuyersGuideArticlePage']:
        return self.get_related_articles()[3:]


class BuyersGuideArticlePageAuthorProfileRelation(
    wagtail_models.TranslatableMixin,
    wagtail_models.Orderable,
):
    """Through model for relation from article page to author profile."""
    page = cluster_fields.ParentalKey(
        'wagtailpages.BuyersGuideArticlePage',
        related_name='author_profile_relations',
    )
    author_profile = models.ForeignKey(
        'wagtailpages.Profile',
        on_delete=models.CASCADE,
        related_name='+',
        null=False,
        blank=False,
    )

    panels = [snippet_panels.SnippetChooserPanel('author_profile')]

    def __str__(self):
        return f'{self.page.title} -> {self.author_profile.name}'


class BuyersGuideArticlePageContentCategoryRelation(
    wagtail_models.TranslatableMixin,
    wagtail_models.Orderable,
):
    """Through model for relation from article page to content category."""
    page = cluster_fields.ParentalKey(
        'wagtailpages.BuyersGuideArticlePage',
        related_name='content_category_relations',
    )
    content_category = models.ForeignKey(
        'wagtailpages.BuyersGuideContentCategory',
        on_delete=models.CASCADE,
        related_name='+',
        null=False,
        blank=False,
    )

    panels = [snippet_panels.SnippetChooserPanel('content_category')]

    def __str__(self):
        return f'{self.page.title} -> {self.content_category.title}'


class BuyersGuideArticlePageRelatedArticleRelation(
    wagtail_models.TranslatableMixin,
    wagtail_models.Orderable,
):
    page = cluster_fields.ParentalKey(
        'wagtailpages.BuyersGuideArticlePage',
        related_name='related_article_relations',
    )
    article = models.ForeignKey(
        'wagtailpages.BuyersGuideArticlePage',
        on_delete=models.CASCADE,
        related_name='+',
        null=False,
        blank=False,
    )

    panels = [panels.PageChooserPanel('article')]

    def __str__(self):
        return f'{self.page.title} -> {self.article.title}'
