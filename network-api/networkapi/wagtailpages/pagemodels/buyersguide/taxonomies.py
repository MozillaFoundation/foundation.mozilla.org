from django.db import models
from wagtail import models as wagtail_models
from wagtail.admin.widgets.slug import SlugInput
from wagtail.admin import panels as admin_panels
from wagtail_localize import fields as localize_fields


class BuyersGuideContentCategory(wagtail_models.TranslatableMixin, models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(
        max_length=100,
        null=False,
        blank=False,
        help_text=(
            "The slug is auto-generated from the title, but can be customized if needed. "
            "It needs to be unique per locale. "
        ),
    )

    panels = [
        admin_panels.TitleFieldPanel("title"),
        admin_panels.FieldPanel("slug", widget=SlugInput),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("title"),
        localize_fields.SynchronizedField("slug"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta):
        ordering = ["title"]
        verbose_name = "Buyers Guide Content Category"
        verbose_name_plural = "Buyers Guide Content Categories"
        unique_together = wagtail_models.TranslatableMixin.Meta.unique_together + [
            ("locale", "slug"),
        ]

    def __str__(self) -> str:
        return self.title

    def validate_unique(self, exclude=None):
        if exclude and "locale" in exclude:
            exclude.remove("locale")
        return super().validate_unique(exclude)
