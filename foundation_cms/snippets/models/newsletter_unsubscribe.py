from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField


@register_snippet
class NewsletterUnsubscribe(TranslatableMixin, models.Model):
    name = models.CharField(
        default="",
        max_length=100,
        help_text="The name of this newsletter unsubscribe form.",
    )
    header = models.CharField(max_length=255, default="Default Header text. Will be updated before launch.")
    description = models.CharField(
        blank=True, max_length=255, help_text="Additional description text below the header."
    )
    button_text = models.CharField(max_length=50, default="Default", help_text="Text to display on the submit button.")

    panels = [
        FieldPanel("name"),
        FieldPanel("header"),
        FieldPanel("description"),
        FieldPanel("button_text"),
    ]

    translatable_fields = [
        SynchronizedField("name"),
        TranslatableField("header"),
        TranslatableField("description"),
        TranslatableField("button_text"),
    ]

    def __str__(self):
        return self.name
