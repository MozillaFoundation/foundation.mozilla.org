from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField


class BaseSignupForm(TranslatableMixin, models.Model):
    """
    Abstract base model for signup forms.
    """

    name = models.CharField(
        default="",
        max_length=100,
        help_text="The name of this signup form.",
    )
    cta_header = models.CharField(max_length=255, default="Stay updated with our latest news and updates.")
    cta_description = models.CharField(
        blank=True, max_length=255, help_text="Additional description text below the header."
    )
    button_text = models.CharField(max_length=50, default="Sign Up", help_text="Text to display on the button.")
    layout = models.CharField(
        max_length=20,
        choices=[
            ("expanded", "Expanded"),
            ("expand_on_focus", "Expand On Focus"),
        ],
        default="expanded",
        help_text="Controls how the form is displayed.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("cta_header"),
        FieldPanel("cta_description"),
        FieldPanel("button_text"),
        FieldPanel("layout"),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_form_type(self):
        """Returns the type of form (i.e. newsletter, pdf_download)."""
        raise NotImplementedError("Subclasses must implement get_form_type")

    base_translatable_fields = [
        SynchronizedField("name"),
        TranslatableField("cta_header"),
        TranslatableField("cta_description"),
        TranslatableField("button_text"),
        SynchronizedField("layout"),
    ]
