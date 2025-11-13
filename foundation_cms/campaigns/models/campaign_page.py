from django.db import models
from django.shortcuts import redirect, render
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models import AbstractBasePage
from foundation_cms.campaigns.blocks import (
    PetitionShareBlock,
    PetitionSignedBlock,
    PetitionThankYouBlock,
)

from .cta_base import CTA


class CampaignPage(AbstractBasePage):
    """
    These pages come with sign-a-petition CTAs
    """

    header = models.CharField(max_length=250, blank=True, help_text="Header for the campaign page")

    cta = models.ForeignKey(
        CTA,
        related_name="campaign_page_for_cta",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose one of our call-to-action snippets, or create a new one.",
    )

    state_signed_content = StreamField(
        [
            ("panel", PetitionSignedBlock()),
        ],
        use_json_field=True,
        blank=True,
        help_text="Content shown after petition is signed",
    )

    state_share_content = StreamField(
        [
            ("panel", PetitionShareBlock()),
        ],
        use_json_field=True,
        blank=True,
        help_text="Content shown when user chooses to share",
    )

    state_thank_you_content = StreamField(
        [
            ("panel", PetitionThankYouBlock()),
        ],
        use_json_field=True,
        blank=True,
        help_text="Final thank you content",
    )

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("cta"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("state_signed_content"),
                FieldPanel("state_share_content"),
                FieldPanel("state_thank_you_content"),
            ],
            heading="Petition Flow Content",
        ),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        TranslatableField("cta"),
        SynchronizedField("state_signed_content"),
        SynchronizedField("state_share_content"),
        SynchronizedField("state_thank_you_content"),
    ]

    subpage_types = [
        "campaigns.CampaignPage",
        "core.GeneralPage",
    ]

    # State managed via URL param ?state=&medium=
    def serve(self, request):
        state = request.GET.get("state", "start")
        medium = request.GET.get("medium", "web")

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "sign":
                # TODO: Save signature to your DB or external CRM
                return redirect(f"{self.url}?state=signed&medium={medium}")

            if action == "share":
                return redirect(f"{self.url}?state=sharing&medium={medium}")

            if action == "donate":
                # TODO: Handle donation logic
                return redirect(f"{self.url}?state=donate&medium={medium}")

            if action == "skip":
                return redirect(f"{self.url}?state=end&medium={medium}")

        return render(
            request,
            self.get_template(request),
            {
                "page": self,
                "state": state,
            },
        )

    class Meta:
        verbose_name = "Campaign Page (New)"
        verbose_name_plural = "Campaign Pages (New)"
