from urllib.parse import urlencode

from django.db import models
from django.shortcuts import redirect, render
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    HelpPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Orderable, Page, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField

from foundation_cms.base.models import AbstractBasePage
from foundation_cms.utils import get_default_locale, localize_queryset

from .petition import Petition


class CampaignPageKeepContributingRelation(TranslatableMixin, Orderable):
    page = ParentalKey(
        "campaigns.CampaignPage",
        related_name="keep_contributing_pages",
        on_delete=models.CASCADE,
    )
    keep_contributing_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        related_name="keep_contributing_relations",
        help_text="Select a page to feature as a keep-contributing link.",
    )

    panels = [
        PageChooserPanel("keep_contributing_page"),
    ]


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

    keep_contributing_topic = models.ForeignKey(
        "base.Topic",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
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
                MultiFieldPanel(
                    [
                        HelpPanel(
                            content=(
                                "<p>"
                                "This section determines which pages appear in the Keep Contributing area. "
                                "It resolves in the following order:<br><br>"
                                "1. <b>Selected pages</b> — if you choose <b>two</b> pages below, "
                                "those will always beshown.<br>"
                                "2. <b>Selected topic</b> — if no pages are chosen but a topic is set, the "
                                "two most recent pages that share that topic will be shown.<br>"
                                "3. <b>Fallback</b> — if neither pages nor a topic are provided, the two "
                                "latest campaign pages will be used.<br>"
                                "</p>"
                            )
                        ),
                        InlinePanel(
                            "keep_contributing_pages",
                            label="Keep contributing pages",
                            max_num=2,
                        ),
                        FieldPanel("keep_contributing_topic"),
                    ],
                    heading="Keep Contributing Section",
                ),
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
        SynchronizedField("keep_contributing_pages"),
        SynchronizedField("keep_contributing_topic"),
    ]

    search_fields = AbstractBasePage.search_fields + [
        index.SearchField("body", boost=8),
        # Campaign topic relationships
        index.RelatedFields(
            "keep_contributing_topic",
            [
                index.SearchField("name", boost=4),
            ],
        ),
        # Campaign filters
        index.FilterField("first_published_at"),
        index.FilterField("live"),
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
        keep_contributing_pages = self.get_keep_contributing_pages()

        context.update(
            {
                "page": self,
                "keep_contributing_pages": keep_contributing_pages,
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

    @cached_property
    def get_selected_keep_contributing_pages(self):
        selected_keep_contributing_pages = Page.objects.filter(keep_contributing_relations__page=self).order_by(
            "keep_contributing_relations__sort_order"
        )

        localized_selected_keep_contributing_pages = localize_queryset(
            selected_keep_contributing_pages,
            preserve_order=True,
        )

        return localized_selected_keep_contributing_pages.specific()

    def get_tag_related_pages(self):
        """
        Return the two latest pages that share this page's keep_contributing_topic.
        """
        topic = self.keep_contributing_topic
        (default_locale, _) = get_default_locale()

        tag_related_pages = (
            Page.objects.live()
            .public()
            .filter(locale=default_locale, topic_relations__tag=topic)
            .exclude(id=self.id)
            .order_by("-first_published_at")
        )

        localized = localize_queryset(tag_related_pages, preserve_order=True)
        return list(localized.specific()[:2])

    def get_fallback_latest_campaigns(self):
        """
        Return the two latest CampaignPages in their localized versions
        """
        (default_locale, _) = get_default_locale()

        default_campaigns = (
            CampaignPage.objects.live()
            .public()
            .filter(locale=default_locale)
            .exclude(id=self.id)
            .order_by("-first_published_at")
        )

        localized_campaigns = localize_queryset(
            default_campaigns,
            preserve_order=True,
        )

        return list(localized_campaigns.specific()[:2])

    def get_keep_contributing_pages(self):
        # 1. If pages have been manually selected for this section, use those.
        if self.keep_contributing_pages.count() == 2:
            return self.get_selected_keep_contributing_pages

        # 2. Else, if a topic is set, use topic-related pages.
        elif self.keep_contributing_topic:
            return self.get_tag_related_pages()

        # 3. Else, fall back to the 2 latest campaigns.
        else:
            return self.get_fallback_latest_campaigns()

    def get_petition_signed_url(self, request):
        base_url = self.get_full_url()
        existing_params = request.GET.dict()
        existing_params["state"] = "signed"
        petition_signed_url = base_url + "?" + urlencode(existing_params)
        return petition_signed_url

    class Meta:
        verbose_name = "Campaign Page (New)"
        verbose_name_plural = "Campaign Pages (New)"
