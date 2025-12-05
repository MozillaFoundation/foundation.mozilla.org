from urllib.parse import urlencode

from django.db import models
from django.shortcuts import redirect, render
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField

from foundation_cms.base.models import AbstractBasePage
from foundation_cms.nothing_personal.models.article_page import (
    NothingPersonalArticlePage,
)
from foundation_cms.utils import get_default_locale, localize_queryset

from .petition import Petition


class CampaignPage(AbstractBasePage):
    """
    These pages come with sign-a-petition CTAs
    """

    header = models.CharField(max_length=250, blank=True, help_text="Header for the campaign page")

    cta = models.ForeignKey(
        Petition,
        related_name="campaign_page_for_cta",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose one of our call-to-action snippets, or create a new one.",
    )

    # --- SIGNED STATE FIELDS ---
    signed_header = models.CharField(
        max_length=200, default="Thank you for signing", help_text="Header shown after petition is signed"
    )

    signed_donation_question = models.CharField(
        max_length=200,
        blank=True,
        default="Would you like to support our work with a donation?",
        help_text="Donation question shown after petition is signed",
    )

    signed_body = RichTextField(
        default="Thank you for signing this petition! "
        "Your voice matters in the fight for a healthier internet. "
        "Would you like to support Mozilla's nonprofit work with a donation?",
        help_text="Content shown after signing",
    )

    # --- SHARING STATE FIELDS ---
    share_header = models.CharField(
        max_length=200, default="Share this with at least one other person", help_text="Header for sharing step"
    )

    share_body = RichTextField(
        default="Mozilla is a nonprofit organization fighting for "
        "a healthy internet, where privacy is included by "
        "design and you have more control over your personal "
        "information. We depend on contributions from people "
        "like you to carry out this work. Can you share this petition?",
        help_text="Content for sharing step",
    )

    # --- THANK YOU STATE FIELDS ---
    thank_you_header = models.CharField(
        max_length=200, default="All done here!", help_text="Final thank you message header"
    )

    thank_you_body = RichTextField(
        default="Mozilla is a nonprofit organization fighting for "
        "a healthy internet, where privacy is included by "
        "design and you have more control over your personal "
        "information. We depend on contributions from people "
        "like you to carry out this work. Thank you for helping us!",
        help_text="Final thank you message",
    )

    thank_you_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional image to show in the thank you step",
    )

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("cta"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("signed_header"),
                FieldPanel("signed_donation_question"),
                FieldPanel("signed_body"),
            ],
            heading="After Signing Content",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("share_header"),
                FieldPanel("share_body"),
            ],
            heading="Sharing Step Content",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("thank_you_header"),
                FieldPanel("thank_you_body"),
                FieldPanel("thank_you_image"),
            ],
            heading="Thank You Content",
            classname="collapsible",
        ),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        SynchronizedField("cta"),
        SynchronizedField("signed_header"),
        SynchronizedField("signed_donation_question"),
        SynchronizedField("signed_body"),
        SynchronizedField("share_header"),
        SynchronizedField("share_body"),
        SynchronizedField("thank_you_header"),
        SynchronizedField("thank_you_body"),
        SynchronizedField("thank_you_image"),
    ]

    subpage_types = [
        "campaigns.CampaignPage",
        "core.GeneralPage",
    ]

    # State managed via URL param ?state=&medium=
    def serve(self, request):
        state = request.GET.get("state", "start")
        medium = request.GET.get("medium", "web")
        user_email = request.GET.get("email", "")

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "share":
                return redirect(f"{self.url}?state=sharing&medium={medium}")

            if action == "skip":
                return redirect(f"{self.url}?state=end&medium={medium}")

        context = self.get_context(request)
        context.update(
            {
                "state": state,
                "medium": medium,
                "user_email": user_email,
            }
        )

        return render(request, self.get_template(request), context)

    def get_context(self, request, *args, **kwargs):
        """Override get_context to add latest articles for More Stories section"""
        context = super().get_context(request, *args, **kwargs)

        localized_cta = self.get_localized_cta()
        latest_articles_list = self.get_keep_contributing_pages()

        context.update(
            {
                "page": self,
                "latest_articles": latest_articles_list,
                "petition_cta": localized_cta,
                "petition_signed_url": self.get_petition_signed_url(request),
            }
        )

        return context

    def get_localized_cta(self):
        petition_cta = None
        petition_cta_localized = None
        if self.cta:
            try:
                petition_cta = Petition.objects.get(id=self.cta.id)
            except Petition.DoesNotExist:
                petition_cta = self.cta

            if petition_cta:
                petition_cta_localized = petition_cta.localized

        return petition_cta_localized

    def get_keep_contributing_pages(self):
        (default_locale, _) = get_default_locale()
        default_articles = (
            NothingPersonalArticlePage.objects.live()
            .public()
            .filter(locale=default_locale)
            .order_by("-first_published_at")
        )
        latest_articles = localize_queryset(default_articles, preserve_order=True)
        latest_articles_list = list(latest_articles.specific()[:2])

        return latest_articles_list

    def get_petition_signed_url(self, request):
        base_url = self.get_full_url()
        existing_params = request.GET.dict()
        existing_params["state"] = "signed"
        petition_signed_url = base_url + "?" + urlencode(existing_params)
        return petition_signed_url

    class Meta:
        verbose_name = "Campaign Page (New)"
        verbose_name_plural = "Campaign Pages (New)"
