import json

from django.db import models
from django.shortcuts import redirect, render
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.fields import (
    StreamFieldPanel,
    SynchronizedField,
    TranslatableField,
)

from foundation_cms.base.models import AbstractBasePage
from foundation_cms.campaigns.blocks import (
    PetitionShareBlock,
    PetitionSignedBlock,
    PetitionThankYouBlock,
)
from foundation_cms.campaigns.models import CTA


class CampaignPage(AbstractBasePage):
    """
    These pages come with sign-a-petition CTAs
    """

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
    )

    state_share_content = StreamField(
        [
            ("panel", PetitionShareBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    state_thank_you_content = StreamField(
        [
            ("panel", PetitionThankYouBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("cta"),
        FieldPanel("body"),
        StreamFieldPanel("state_signed_content"),
        StreamFieldPanel("state_share_content"),
        StreamFieldPanel("state_thank_you_content"),
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

    # State managed via URL param ?state=
    def serve(self, request):
        state = request.GET.get("state", "start")

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "sign":
                return redirect(f"{self.url}?state=signed")

            if action == "share":
                return redirect(f"{self.url}?state=sharing")

            if action == "donate":
                return redirect(f"{self.url}?state=donate")

            if action == "dismiss":
                return redirect(self.url)

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
