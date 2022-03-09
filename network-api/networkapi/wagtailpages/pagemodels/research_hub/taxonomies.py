from django.db import models
from wagtail.admin import edit_handlers
from wagtail.snippets import models as snippet_models


@snippet_models.register_snippet
class ResearchRegion(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    panels = [
        edit_handlers.FieldPanel('name'),
    ]

    def __str__(self):
        return self.name


@snippet_models.register_snippet
class ResearchTopic(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=True)

    panels = [
        edit_handlers.FieldPanel('name'),
        edit_handlers.FieldPanel('description'),
    ]

    def __str__(self):
        return self.name
