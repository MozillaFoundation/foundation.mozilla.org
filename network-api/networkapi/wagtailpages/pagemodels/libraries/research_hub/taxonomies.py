from django.db import models
from wagtail.admin import panels as wagtail_panels

from networkapi.wagtailpages.pagemodels.taxonomy import BaseTaxonomy


class ResearchRegion(BaseTaxonomy):
    pass


class ResearchTopic(BaseTaxonomy):
    description = models.TextField(null=False, blank=True)

    panels = BaseTaxonomy.panels + [
        wagtail_panels.FieldPanel("description"),
    ]
