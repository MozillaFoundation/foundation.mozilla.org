from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index


class BaseTaxonomy(TranslatableMixin):
    name = models.CharField(max_length=50, null=False, blank=False)

    panels = [
        FieldPanel("name"),
    ]

    class Meta(TranslatableMixin.Meta):
        abstract = True
        ordering = ["name"]

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.FilterField("locale_id"),
    ]

    def __str__(self):
        return self.name
