from django.db import models
from wagtail.admin import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index


class BaseTaxonomy(TranslatableMixin):
    name = models.CharField(max_length=70, blank=False)

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        abstract = True

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.FilterField("locale_id"),
    ]

    def __str__(self):
        return self.name
