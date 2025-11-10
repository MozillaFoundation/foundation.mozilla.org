import json
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models import AbstractBasePage
from foundation_cms.snippets.models import DonateBanner
from .cta_base import CTA


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
    
    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("cta"),
        InlinePanel("donation_modals", label="Campaign Donation Modals", max_num=4),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        TranslatableField("donation_modals"),
    ]

    subpage_types = [
        "campaigns.CampaignPage",
        "core.GeneralPage",
    ]

    template = "campaigns/campaign_page.html"

    def get_donation_modal_json(self):
        """
        Safe method for React compatibility
        Returns JSON that maps DonateBanner data to legacy modal format
        """
        modals = self.donation_modals.all()
        if not modals.exists():
            return "[]"
        
        try:
            modals_json = [modal.to_simple_dict() for modal in modals]
            return json.dumps(modals_json)
        except Exception as e:
            print(f"Error serializing donation modals: {e}")
            return "[]"

    def get_context(self, request, *args, **kwargs):
        """Add both global banner and campaign modals"""
        context = super().get_context(request, *args, **kwargs)
        
        context.update({
            'donation_modal_json': self.get_donation_modal_json(),
            'has_campaign_modals': self.donation_modals.exists(),
        })
        
        return context

    class Meta:
        verbose_name = "Campaign Page (New)"
        verbose_name_plural = "Campaign Pages (New)"
