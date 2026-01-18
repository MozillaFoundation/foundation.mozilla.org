from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.models import Page

from foundation_cms.core.models.home_page import HomePage
from foundation_cms.snippets.models.newsletter_signup import NewsletterSignup


class SitewideFooterNewsletterSignupPage(Page):
    max_count = 1

    newsletter_signup = models.ForeignKey(
        NewsletterSignup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sitewide_footer_newsletter_signup",
        help_text=(
            "CTA Banner rendered at the top of the page site-wide. "
            "Note: A/B testing of this banner will also be site-wide and across all locales."
        ),
    )

    content_panels = [
        HelpPanel(
            content=mark_safe(
                "<p>This page is where you can select a <strong>Newsletter Signup</strong> snippet "
                "and have it render on the footer sitewide. Feel free to name the title of this page whatever "
                "you would like, as it's just for use in the CMS only.</p>"
                "<p>To run an <strong>A/B test</strong> between two newsletter signup snippets, publish this "
                "page with the signup you would like to use as 'control', then select a new newsletter signup "
                "that you would like to use for your variant, and click "
                "<strong>Save and Create A/B test</strong>.</p>"
                "<p><strong>Note:</strong> Please do not translate this page.</p>"
            )
        ),
        FieldPanel("title", help_text="The page title as you'd like it to be seen in the CMS."),
        MultiFieldPanel(
            [
                FieldPanel("newsletter_signup"),
            ],
            heading="Newsletter Signup",
            classname="collapsible",
        ),
    ]

    promote_panels: list = []

    subpage_types: list = []

    parent_page_types = [HomePage]

    template = "patterns/components/previews/footer_newsletter_signup.html"

    class Meta:
        verbose_name = "Footer Newsletter Signup Page"
        verbose_name_plural = "Footer Newsletter Signup Pages"

    # Override the context for template purposes
    def get_context(self, request):
        context = super().get_context(request)
        context["object"] = self.newsletter_signup
        return context


@receiver(post_delete, sender=SitewideFooterNewsletterSignupPage)
def delete_all_footer_newsletter_signup_page_translations(sender, instance, **kwargs):
    """
    Deletes all translated instances of the SitewideFooterNewsletterSignupPage, as they don't auto-delete.
    This prevents lingering aliases from blocking the creation of a new SitewideFooterNewsletterSignupPage
    due to the max_count=1 limit.
    """
    SitewideFooterNewsletterSignupPage.objects.all().delete()
