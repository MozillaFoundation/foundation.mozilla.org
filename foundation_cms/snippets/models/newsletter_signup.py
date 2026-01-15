from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from .base_signup_form import BaseSignupForm


@register_snippet
class NewsletterSignup(BaseSignupForm):
    panels = BaseSignupForm.panels

    def get_form_type(self):
        return "newsletter"

    translatable_fields = BaseSignupForm.base_translatable_fields


@register_setting(icon="mail")
class FooterNewsletterSignup(BaseSiteSetting):
    select_related = ["newsletter_signup"]

    newsletter_signup = models.ForeignKey(
        "snippets.NewsletterSignup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Footer Newsletter Signup",
        help_text="Select a newsletter signup to appear in the footer.",
    )

    content_panels = [
        FieldPanel("newsletter_signup"),
    ]

    class Meta:
        verbose_name = "Footer Newsletter Signup (New)"
        verbose_name_plural = "Footer Newsletter Signups (New)"
