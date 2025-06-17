from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet


@register_snippet
class NewsletterSignup(models.Model):
    name = models.CharField(
        default="",
        max_length=100,
        help_text="The name of this newsletter signup form.",
    )
    cta_text = models.CharField(max_length=255, default="Stay updated with our latest news and updates.")
    button_text = models.CharField(max_length=50, default="Sign Up", help_text="Text to display on the signup button.")
    newsletter = models.CharField(
        max_length=100,
        help_text="The (pre-existing) newsletter to sign up for.",
        default="mozilla-foundation",
    )
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
        FieldPanel("cta_text"),
        FieldPanel("button_text"),
        FieldPanel("newsletter"),
        FieldPanel("layout"),
    ]

    def __str__(self):
        return self.name


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
