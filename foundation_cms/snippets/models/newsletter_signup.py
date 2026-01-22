from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField

from .base_signup_form import BaseSignupForm


@register_snippet
class NewsletterSignup(BaseSignupForm):
    newsletter = models.CharField(
        max_length=100,
        help_text="The (pre-existing) newsletter to sign up for.",
        default="mozillafoundationorg",
    )

    panels = BaseSignupForm.panels + [
        FieldPanel("newsletter"),
    ]

    def get_form_type(self):
        return "newsletter"

    translatable_fields = BaseSignupForm.base_translatable_fields + [
        SynchronizedField("newsletter"),
    ]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("translation_key", "locale"), name="unique_translation_key_locale_snippets_newslettersignup"
            )
        ]
        verbose_name = "Newsletter Signup"
        verbose_name_plural = "Newsletter Signups"


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
