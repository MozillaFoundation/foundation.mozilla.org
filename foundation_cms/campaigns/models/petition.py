from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from .cta_base import CTA


@register_snippet
class Petition(TranslatableMixin, CTA):
    campaign_id = models.CharField(
        max_length=20,
        help_text="Which Salesforce Campaign ID should this petition be tied to?",
        null=True,
        blank=True,
    )

    show_country_field = models.BooleanField(
        default=False,
        verbose_name="Show country field?",
        help_text="This toggles the visibility of the optional country dropdown field.",
    )

    show_postal_code_field = models.BooleanField(
        default=False,
        verbose_name="Show postal code field?",
        help_text="This toggles the visibility of the optional postal code field.",
    )

    show_comment_field = models.BooleanField(
        default=False,
        verbose_name="Show comment field?",
        help_text="This toggles the visibility of the optional comment field.",
    )

    share_link = models.URLField(
        max_length=1024,
        help_text="Link that will be put in share button",
        blank=True,
        editable=False,
    )

    share_bluesky = models.CharField(
        max_length=20,
        help_text="Share Progress id for bluesky button",
        blank=True,
    )

    share_facebook = models.CharField(
        max_length=20,
        help_text="Share Progress id for facebook button",
        blank=True,
    )

    share_email = models.CharField(
        max_length=20,
        help_text="Share Progress id for email button",
        blank=True,
    )

    thank_you = models.CharField(
        max_length=140,
        help_text="Message to show after thanking people for signing",
        default="Thank you for signing too!",
    )

    translatable_fields = [
        SynchronizedField("show_country_field"),
        SynchronizedField("show_postal_code_field"),
        SynchronizedField("show_comment_field"),
        SynchronizedField("share_bluesky"),
        SynchronizedField("share_facebook"),
        SynchronizedField("share_email"),
        TranslatableField("thank_you"),
        TranslatableField("header"),
        TranslatableField("description"),
    ]

    search_fields = CTA.search_fields + [
        index.SearchField("campaign_id", boost=2),
        index.FilterField("locale_id"),
        index.FilterField("show_country_field"),
        index.FilterField("show_postal_code_field"),
        index.FilterField("show_comment_field"),
    ]

    panels = CTA.panels + [
        FieldPanel("campaign_id"),
        FieldPanel("show_country_field"),
        FieldPanel("show_postal_code_field"),
        FieldPanel("show_comment_field"),
        FieldPanel("share_bluesky"),
        FieldPanel("share_facebook"),
        FieldPanel("share_email"),
        FieldPanel("thank_you"),
    ]

    class Meta(TranslatableMixin.Meta):
        ordering = ["-id"]
        verbose_name = "Petition (New)"
        verbose_name_plural = "Petitions (New)"
