from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail_localize import fields as localize_fields


class BaseTaxonomy(TranslatableMixin):
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(
        max_length=100,
        null=False,
        blank=False,
        help_text=(
            "The slug is auto-generated from the name, but can be customized if needed. "
            "It needs to be unique per locale."
        ),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta(TranslatableMixin.Meta):
        abstract = True
        ordering = ["name"]
        unique_together = TranslatableMixin.Meta.unique_together + [
            ("locale", "slug"),
        ]

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.FilterField("locale_id"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("name"),
        localize_fields.SynchronizedField("slug"),
    ]

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if exclude and "locale" in exclude:
            exclude.remove("locale")
        return super().validate_unique(exclude)
