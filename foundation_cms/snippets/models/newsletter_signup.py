from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


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
        help_text="Select a newsletter signup to appear in the footer."
    )

    content_panels = [
        FieldPanel("newsletter_signup"),
    ]

    class Meta:
        verbose_name = "Newsletter Signup"
        verbose_name_plural = "Newsletter Signups"
