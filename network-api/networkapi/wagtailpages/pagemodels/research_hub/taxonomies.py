from django.db import models
from wagtail.admin import panels as edit_handlers
from wagtail.snippets import models as snippet_models

from networkapi.wagtailpages.pagemodels.taxonomy import BaseTaxonomy


@snippet_models.register_snippet
class ResearchRegion(BaseTaxonomy):
    pass


@snippet_models.register_snippet
class ResearchTopic(BaseTaxonomy):
    description = models.TextField(null=False, blank=True)

    panels = BaseTaxonomy.panels + [
        edit_handlers.FieldPanel("description"),
    ]
