from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)


class HelpPageNotice(TranslatableMixin, models.Model):
    name = models.CharField(max_length=50, help_text="What will this notice be called in the CMS?")

    text = RichTextField(
        features=base_rich_text_options,
    )
    notice_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Notice Image",
    )
    notice_image_alt_text = models.CharField(
        max_length=50, blank=True, help_text="Image description (for screen readers)."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("text"),
        FieldPanel("notice_image"),
        FieldPanel("notice_image_alt_text"),
    ]

    translatable_fields = [
        SynchronizedField("name"),
        TranslatableField("text"),
        SynchronizedField("notice_image"),
        TranslatableField("notice_image_alt_text"),
    ]

    def __str__(self):
        return self.name
