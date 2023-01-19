from django.db import models
from modelcluster import fields as cluster_fields
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel


class ResearchAuthorRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="research_authors",
    )
    author_profile = models.ForeignKey(
        "wagtailpages.Profile",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="authored_research",
    )

    panels = [
        FieldPanel("author_profile"),
    ]


class ResearchDetailPageResearchRegionRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_regions",
    )
    research_region = models.ForeignKey(
        "wagtailpages.ResearchRegion",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_research",
    )

    panels = [
        FieldPanel("research_region"),
    ]


class ResearchDetailPageResearchTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_topics",
    )
    research_topic = models.ForeignKey(
        "wagtailpages.ResearchTopic",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_research",
    )

    panels = [
        FieldPanel("research_topic"),
    ]


class ResearchLandingPageFeaturedResearchTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    research_landing_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchLandingPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="featured_topics",
    )
    research_topic = models.ForeignKey(
        "wagtailpages.ResearchTopic",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("research_topic"),
    ]
