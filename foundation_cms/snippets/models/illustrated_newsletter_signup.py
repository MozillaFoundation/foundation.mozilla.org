from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField


@register_snippet
class IllustratedNewsletterSignup(TranslatableMixin, models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Identify this newsletter signup for editors. This name is not displayed.",
    )
    heading = models.CharField(
        max_length=60,
        help_text="Heading displayed above the newsletter signup form. Maximum 60 characters.",
    )
    illustration = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional decorative illustration displayed above the heading.",
    )
    newsletter = models.CharField(
        max_length=100,
        help_text="The identifier of the pre-existing newsletter to sign up for.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("heading"),
        FieldPanel("illustration"),
        FieldPanel("newsletter"),
    ]

    translatable_fields = [
        SynchronizedField("name"),
        TranslatableField("heading"),
        SynchronizedField("illustration"),
        SynchronizedField("newsletter"),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Illustrated Newsletter Signup"
        verbose_name_plural = "Illustrated Newsletter Signups"

    def __str__(self):
        return self.name
