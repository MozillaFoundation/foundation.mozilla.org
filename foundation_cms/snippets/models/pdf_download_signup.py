from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import TranslatableField

from .base_signup_form import BaseSignupForm


@register_snippet
class PdfDownloadSignup(BaseSignupForm):
    pdf_title = models.CharField(max_length=255, help_text="Title of the PDF document", default="")
    pdf_description = models.TextField(blank=True, help_text="Description of the PDF content")

    panels = BaseSignupForm.panels + [
        FieldPanel("pdf_title"),
        FieldPanel("pdf_description"),
    ]

    def get_form_type(self):
        return "pdf_download"

    translatable_fields = BaseSignupForm.base_translatable_fields + [
        TranslatableField("pdf_title"),
        TranslatableField("pdf_description"),
    ]

    class Meta:
        verbose_name = "PDF Download Signup"
        verbose_name_plural = "PDF Download Signups"
