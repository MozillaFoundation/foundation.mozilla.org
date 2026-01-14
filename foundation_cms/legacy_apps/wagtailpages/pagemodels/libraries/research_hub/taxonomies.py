from django.db import models
from wagtail.admin import panels as wagtail_panels

from foundation_cms.legacy_apps.wagtailpages.pagemodels.taxonomy import BaseTaxonomy


class ResearchRegion(BaseTaxonomy):
    class Meta(BaseTaxonomy.Meta):
        verbose_name = "Research Region (Legacy)"
        verbose_name_plural = "Research Regions (Legacy)"


class ResearchTopic(BaseTaxonomy):
    description = models.TextField(null=False, blank=True)

    panels = BaseTaxonomy.panels + [
        wagtail_panels.FieldPanel("description"),
    ]

    class Meta(BaseTaxonomy.Meta):
        verbose_name = "Research Topic (Legacy)"
        verbose_name_plural = "Research Topics (Legacy)"
