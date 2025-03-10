from django.db import models
from modelcluster import fields as cluster_fields
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel


class ResearchAuthorRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    detail_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="authors",
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


class ResearchLandingPageFeaturedAuthorsRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    landing_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchLandingPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="featured_authors",
    )
    author = models.ForeignKey(
        "wagtailpages.Profile",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("author"),
    ]


class ResearchDetailPageResearchRegionRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    detail_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_regions",
    )
    region = models.ForeignKey(
        "wagtailpages.ResearchRegion",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_research",
    )

    panels = [
        FieldPanel("region"),
    ]


class ResearchDetailPageResearchTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    detail_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_topics",
    )
    topic = models.ForeignKey(
        "wagtailpages.ResearchTopic",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_research",
    )

    panels = [
        FieldPanel("topic"),
    ]


class ResearchLandingPageFeaturedResearchTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    landing_page = cluster_fields.ParentalKey(
        "wagtailpages.ResearchLandingPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="featured_topics",
    )
    topic = models.ForeignKey(
        "wagtailpages.ResearchTopic",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("topic"),
    ]
