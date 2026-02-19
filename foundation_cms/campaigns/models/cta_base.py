from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.constants import DEFAULT_RICH_TEXT_FEATURES, RICH_TEXT_BASE_OPTIONS


class CTABase(TranslatableMixin, models.Model):
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

    description = RichTextField(
        help_text="Body (richtext) of component",
        blank=True,
        features=DEFAULT_RICH_TEXT_FEATURES,
    )

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

    donate_text = models.CharField(
        max_length=150,
        help_text="Donate button label",
        default="Yes, I'll chip in $10",
        blank=True,
    )

    donate_url = models.CharField(
        max_length=255,
        default="?form=donate",
        blank=True,
        help_text=(
            "Donate button URL. Use ?form=donate for Mozilla donate form, " "or full URL for external donation page."
        ),
    )

    translatable_fields = [
        TranslatableField("name"),
        TranslatableField("header"),
        TranslatableField("description"),
        TranslatableField("privacy_notice"),
        SynchronizedField("newsletter"),
        TranslatableField("donate_text"),
        SynchronizedField("donate_url"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("newsletter"),
        FieldPanel("header"),
        FieldPanel("description"),
        FieldPanel("privacy_notice"),
        MultiFieldPanel(
            [
                FieldPanel("donate_text"),
                FieldPanel("donate_url"),
            ],
            heading="Donation Settings",
            classname="collapsible",
        ),
    ]

    search_fields = [
        index.SearchField("name", boost=6),
        index.SearchField("header", boost=6),
        index.SearchField("description", boost=4),
        index.SearchField("newsletter", boost=2),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        abstract = True


@register_snippet
class CTA(CTABase):
    """Concrete CTA base for other CTAs"""

    panels = CTABase.panels

    class Meta(TranslatableMixin.Meta):
        ordering = ["-id"]
        verbose_name = "CTA"
        verbose_name_plural = "CTAs"
