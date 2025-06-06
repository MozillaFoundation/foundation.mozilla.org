from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


@register_snippet
class NewsletterSignup(models.Model):
    cta_text = models.CharField(
        max_length=255,
        default="Stay updated with our latest news and updates."
    )
    button_text = models.CharField(
        max_length=50,
        default="Sign Up",
        help_text="Text to display on the signup button."
    )

    panels = [
        FieldPanel("cta_text"),
        FieldPanel("button_text"),
    ]

    def __str__(self):
        return self.cta_text
