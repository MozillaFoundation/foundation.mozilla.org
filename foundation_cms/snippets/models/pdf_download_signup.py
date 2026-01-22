from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField

from .base_signup_form import BaseSignupForm


@register_snippet
class PdfDownloadSignup(BaseSignupForm):
    smart_email_id = models.CharField(
        max_length=100,
        help_text="The (pre-existing) CaMo template ID for the PDF download signup.",
        default="2d306f6b-1998-49dd-8ebe-fd4b85cf73f6",
    )

    panels = BaseSignupForm.panels + [
        FieldPanel("smart_email_id"),
    ]

    def get_form_type(self):
        return "pdf_download"

    translatable_fields = BaseSignupForm.base_translatable_fields + [
        SynchronizedField("smart_email_id"),
    ]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("translation_key", "locale"), name="unique_translation_key_locale_snippets_pdfdownloadsignup"
            )
        ]
        verbose_name = "PDF Download Signup"
        verbose_name_plural = "PDF Download Signups"
