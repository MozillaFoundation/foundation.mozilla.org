from django.db import models
from modelcluster import fields as cluster_fields
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel


class RCCAuthorRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    rcc_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.RCCDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="rcc_authors",
    )
    author_profile = models.ForeignKey(
        "wagtailpages.Profile",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="authored_rcc_articles",
    )

    panels = [
        FieldPanel("author_profile"),
    ]


class RCCLandingPageFeaturedRCCContentTypeRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    rcc_landing_page = cluster_fields.ParentalKey(
        "wagtailpages.RCCLandingPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="featured_content_types",
    )
    content_type = models.ForeignKey(
        "wagtailpages.RCCContentType",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("content_type"),
    ]


class RCCDetailPageRCCContentTypeRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    rcc_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.RCCDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_content_types",
    )
    content_type = models.ForeignKey(
        "wagtailpages.RCCContentType",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_rcc_articles",
    )

    panels = [
        FieldPanel("content_type"),
    ]


class RCCDetailPageRCCTopicRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    rcc_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.RCCDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_topics",
    )
    rcc_topic = models.ForeignKey(
        "wagtailpages.RCCTopic",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_rcc_articles",
    )

    panels = [
        FieldPanel("rcc_topic"),
    ]


class RCCDetailPageRCCCurricularAreaRelation(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    rcc_detail_page = cluster_fields.ParentalKey(
        "wagtailpages.RCCDetailPage",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_curricular_areas",
    )
    curricular_area = models.ForeignKey(
        "wagtailpages.RCCCurricularArea",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="related_rcc_articles",
    )

    panels = [
        FieldPanel("curricular_area"),
    ]
