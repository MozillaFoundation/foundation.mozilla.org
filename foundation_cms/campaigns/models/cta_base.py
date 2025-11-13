from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.constants import RICH_TEXT_BASE_OPTIONS


class CTABase(models.Model):
    name = models.CharField(
        default="",
        max_length=100,
        help_text="Identify this component for other editors",
    )

    header = models.CharField(
        max_length=500,
        help_text="Heading that will display on page for this component",
        blank=True,
    )

    description = RichTextField(help_text="Body (richtext) of component", blank=True)

    privacy_notice = RichTextField(
        help_text="This optional privacy notice field will overwrite the default privacy notice text. "
        "If this field is left blank, the default privacy notice text is used.",
        features=RICH_TEXT_BASE_OPTIONS,
        blank=True,
    )

    newsletter = models.CharField(
        max_length=100,
        help_text="The (pre-existing) newsletter to sign up for",
        default="mozilla-foundation",
    )

    translatable_fields = [
        TranslatableField("name"),
        TranslatableField("header"),
        TranslatableField("description"),
        TranslatableField("privacy_notice"),
        SynchronizedField("newsletter"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("newsletter"),
        FieldPanel("header"),
        FieldPanel("description"),
        FieldPanel("privacy_notice"),
    ]

    search_fields = [
        index.SearchField("name", boost=10),
        index.SearchField("newsletter"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CTA(CTABase):
    """Concrete CTA base for other CTAs"""

    panels = CTABase.panels

    class Meta:
        ordering = ["-id"]
        verbose_name = "CTA (New)"
        verbose_name_plural = "CTAs (New)"
