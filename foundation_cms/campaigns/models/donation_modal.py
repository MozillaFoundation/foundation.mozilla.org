import json
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import TranslatableMixin, Orderable
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.snippets.models import DonateBanner


class CampaignDonationModal(TranslatableMixin, Orderable):

    page = ParentalKey(
        "campaigns.CampaignPage",
        on_delete=models.CASCADE,
        related_name="donation_modals",
    )

    donate_banner = models.ForeignKey(
        DonateBanner,
        on_delete=models.CASCADE,
        help_text="Choose a donation banner for this campaign modal"
    )
    
    modal_trigger = models.CharField(
        max_length=20,
        choices=[
            ("auto", "Auto-show after delay"),
            ("scroll", "Show on scroll percentage"),
            ("exit", "Show on exit intent"),
            ("button", "Show on button click"),
            ("petition_success", "Show after petition submission"),
        ],
        default="petition_success",
        help_text="When to show this modal"
    )
    
    trigger_delay = models.IntegerField(
        default=3,
        help_text="Seconds delay (for auto) or scroll % (for scroll)"
    )

    # Legacy compatibility fields
    dismiss_text = models.CharField(
        max_length=150,
        help_text="Dismiss button label",
        default="No thanks",
    )

    def to_simple_dict(self):
        """Convert to format expected by React components - maps DonateBanner to legacy format"""
        return {
            # Map the DonateBanner fields to legacy DonationModal format
            "name": self.donate_banner.name or f"Modal {self.id}",
            "header": self.donate_banner.title,
            "body": self.donate_banner.subtitle or self.donate_banner.description,
            "donate_text": self.donate_banner.cta_button_text,
            "donate_url": self.donate_banner.cta_link,
            "dismiss_text": self.dismiss_text,
            # Modal-specific behavior for JavaScript
            "trigger": self.modal_trigger,
            "delay": self.trigger_delay,
        }

    panels = [
        MultiFieldPanel([
            FieldPanel("donate_banner"),
        ], heading="Donation Content"),
        MultiFieldPanel([
            FieldPanel("modal_trigger"),
            FieldPanel("trigger_delay"),
            FieldPanel("dismiss_text"),
        ], heading="Modal Behavior"),
    ]

    translatable_fields = [
        TranslatableField("donate_banner"),
        SynchronizedField("modal_trigger"),
        SynchronizedField("trigger_delay"),
        TranslatableField("dismiss_text"),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Campaign Donation Modal"
        verbose_name_plural = "Campaign Donation Modals"
