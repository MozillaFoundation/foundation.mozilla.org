from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from .cta_base import CTA


@register_snippet
class Petition(CTA):
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

    cta_button_text = models.CharField(
        max_length=50,
        default="Add my name",
        help_text="Text for the petition submission button",
    )

    share_twitter = models.CharField(
        max_length=20, help_text="Share Progress id for twitter button, including the sp_... prefix", null=True
    )

    share_facebook = models.CharField(
        max_length=20, help_text="Share Progress id for facebook button, including the sp_... prefix", null=True
    )

    share_email = models.CharField(
        max_length=20, help_text="Share Progress id for email button, including the sp_... prefix", null=True
    )

    translatable_fields = [
        SynchronizedField("show_country_field"),
        SynchronizedField("show_postal_code_field"),
        SynchronizedField("show_comment_field"),
        TranslatableField("header"),
        TranslatableField("description"),
        TranslatableField("cta_button_text"),
        SynchronizedField("share_twitter"),
        SynchronizedField("share_facebook"),
        SynchronizedField("share_email"),
    ]

    search_fields = CTA.search_fields + [
        index.SearchField("description", boost=6),
        index.SearchField("campaign_id", boost=2),
        # Petition filters
        index.FilterField("locale_id"),
    ]

    panels = CTA.panels + [
        FieldPanel("campaign_id"),
        FieldPanel("show_country_field"),
        FieldPanel("show_postal_code_field"),
        FieldPanel("show_comment_field"),
        FieldPanel("cta_button_text"),
        FieldPanel("share_twitter"),
        FieldPanel("share_facebook"),
        FieldPanel("share_email"),
    ]

    class Meta:
        ordering = ["-id"]
        verbose_name = "Petition"
        verbose_name_plural = "Petitions"
