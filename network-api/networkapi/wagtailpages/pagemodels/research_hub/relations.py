from django.db import models
from modelcluster import fields as cluster_fields
from wagtail.core import models as wagtail_models
from wagtail.snippets import edit_handlers as snippet_handlers


class ResearchAuthorRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        'wagtailpages.ResearchDetailPage',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='research_authors',
    )
    author_profile = models.ForeignKey(
        'wagtailpages.Profile',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='authored_research',
    )

    panels = [
        snippet_handlers.SnippetChooserPanel('author_profile'),
    ]


class ResearchDetailPageResearchRegionRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        'wagtailpages.ResearchDetailPage',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='related_regions',
    )
    research_region = models.ForeignKey(
        'wagtailpages.ResearchRegion',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='related_research',
    )

    panels = [
        snippet_handlers.SnippetChooserPanel('research_region'),
    ]


class ResearchDetailPageResearchTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        'wagtailpages.ResearchDetailPage',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='related_topics',
    )
    research_topic = models.ForeignKey(
        'wagtailpages.ResearchTopic',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='related_research',
    )

    panels = [
        snippet_handlers.SnippetChooserPanel('research_topic'),
    ]


class ResearchLandingPageFeaturedResearchTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        'wagtailpages.ResearchLandingPage',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='featured_topics',
    )
    research_topic = models.ForeignKey(
        'wagtailpages.ResearchTopic',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    panels = [
        snippet_handlers.SnippetChooserPanel('research_topic'),
    ]
