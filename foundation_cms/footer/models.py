from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail_localize.fields import SynchronizedField, TranslatableField


class SiteFooter(
    wagtail_models.PreviewableMixin,
    wagtail_models.DraftStateMixin,
    wagtail_models.RevisionMixin,
    wagtail_models.TranslatableMixin,
    ClusterableModel,
):
    """
    Site footer configuration.
    Contains internal/external links, social links, legal text, and display options.
    """

    title = models.CharField(max_length=100, help_text="For internal identification only (e.g. 'Main Footer')")

    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Custom logo for footer (default: Mozilla Foundation wordmark)",
    )

    logo_link_url = models.CharField(
        max_length=500,
        default="/",
        help_text="URL when clicking the footer logo (default: homepage)",
    )

    show_donate_button = models.BooleanField(
        default=True,
        help_text="Show the Donate button in footer",
    )

    donate_button_text = models.CharField(
        max_length=50,
        default="Donate",
        blank=True,
        help_text="Text for the donate button",
    )

    donate_button_url = models.CharField(
        max_length=500,
        default="?form=donate-footer",
        help_text="URL or query parameter for donate form",
    )

    show_language_switcher = models.BooleanField(
        default=True,
        help_text="Show language switcher in footer",
    )

    show_newsletter_signup = models.BooleanField(
        default=True,
        help_text="Show newsletter signup form in footer",
    )

    legal_text = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        help_text="Legal disclaimer text shown at the bottom of the footer",
    )

    panels = [
        panels.HelpPanel(content="To enable a footer on a site, go to Settings > Site Footer."),
        panels.FieldPanel("title"),
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("logo"),
                panels.FieldPanel("logo_link_url"),
            ],
            heading="Logo & Branding",
        ),
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("show_newsletter_signup"),
                panels.FieldPanel("show_language_switcher"),
                panels.FieldPanel("show_donate_button"),
                panels.FieldPanel("donate_button_text"),
                panels.FieldPanel("donate_button_url"),
            ],
            heading="Display Options",
        ),
        panels.MultiFieldPanel(
            [
                panels.InlinePanel(
                    "internal_links", label="Internal Links", max_num=10, help_text="Links to internal pages (max 10)"
                ),
            ],
            heading="Internal Navigation",
        ),
        panels.MultiFieldPanel(
            [
                panels.InlinePanel(
                    "external_links", label="External Links", max_num=10, help_text="Links to external sites (max 10)"
                ),
            ],
            heading="External Links",
        ),
        panels.MultiFieldPanel(
            [
                panels.InlinePanel(
                    "social_links", label="Social Media Links", max_num=10, help_text="Social media links (max 10)"
                ),
            ],
            heading="Social Media",
        ),
        panels.FieldPanel("legal_text"),
    ]

    translatable_fields = [
        SynchronizedField("title"),
        TranslatableField("logo"),
        SynchronizedField("logo_link_url"),
        SynchronizedField("show_donate_button"),
        TranslatableField("donate_button_text"),
        SynchronizedField("donate_button_url"),
        SynchronizedField("show_language_switcher"),
        SynchronizedField("show_newsletter_signup"),
        TranslatableField("internal_links"),
        TranslatableField("external_links"),
        TranslatableField("social_links"),
        TranslatableField("legal_text"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta):
        verbose_name = "Site Footer"
        verbose_name_plural = "Site Footers"

    def __str__(self) -> str:
        return self.title

    def get_preview_template(self, request, mode_name):
        """Return a simple preview template for footer."""
        return "patterns/components/footer/preview.html"

    def get_preview_context(self, request, mode_name):
        """Return context for footer preview."""
        context = super().get_preview_context(request, mode_name)
        context["footer"] = self
        return context


class FooterLink(wagtail_models.Orderable, wagtail_models.TranslatableMixin):
    """
    Base class for footer links (internal/external).
    Uses Orderable for drag-and-drop sorting in admin.
    """

    footer = ParentalKey(
        SiteFooter,
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
    )

    label = models.CharField(max_length=100, help_text="Link text displayed to users")

    url = models.CharField(max_length=500, help_text="URL for this link")

    panels = [
        panels.FieldPanel("label"),
        panels.FieldPanel("url"),
    ]

    translatable_fields = [
        TranslatableField("label"),
        SynchronizedField("url"),
    ]

    class Meta:
        abstract = True
        ordering = ["sort_order"]

    def __str__(self):
        return self.label


class FooterInternalLink(FooterLink):
    """Internal navigation links in footer (e.g., /meet-mozilla/)"""

    footer = ParentalKey(SiteFooter, on_delete=models.CASCADE, related_name="internal_links")

    panels = [
        panels.FieldPanel("label"),
        panels.FieldPanel("url", help_text="Relative URL (e.g. /meet-mozilla/)"),
    ]

    class Meta(FooterLink.Meta):
        verbose_name = "Internal Link"
        verbose_name_plural = "Internal Links"
        constraints = [
            models.UniqueConstraint(
                fields=["translation_key", "locale"],
                name="unique_translation_key_locale_footer_footerinternallink",
            )
        ]


class FooterExternalLink(FooterLink):
    """External links in footer (e.g. https://mozilla.org/careers)"""

    footer = ParentalKey(SiteFooter, on_delete=models.CASCADE, related_name="external_links")

    panels = [
        panels.FieldPanel("label"),
        panels.FieldPanel("url", help_text="Full URL including https://"),
    ]

    class Meta(FooterLink.Meta):
        verbose_name = "External Link"
        verbose_name_plural = "External Links"
        constraints = [
            models.UniqueConstraint(
                fields=["translation_key", "locale"],
                name="unique_translation_key_locale_footer_footerexternallink",
            )
        ]


class FooterSocialLink(wagtail_models.Orderable, wagtail_models.TranslatableMixin):
    """
    Social media links with platform selection.
    Platform determines the icon displayed.
    """

    SOCIAL_PLATFORMS = [
        ("bluesky", "Bluesky"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("spotify", "Spotify"),
        ("tiktok", "TikTok"),
    ]

    footer = ParentalKey(SiteFooter, on_delete=models.CASCADE, related_name="social_links")

    platform = models.CharField(max_length=50, choices=SOCIAL_PLATFORMS, help_text="Select social media platform")

    url = models.URLField(help_text="Full URL to your social media profile")

    panels = [
        panels.FieldPanel("platform"),
        panels.FieldPanel("url"),
    ]

    translatable_fields = [
        SynchronizedField("platform"),
        SynchronizedField("url"),
    ]

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"
        constraints = [
            models.UniqueConstraint(
                fields=["translation_key", "locale"],
                name="unique_translation_key_locale_footer_footersociallink",
            )
        ]

    def __str__(self):
        return f"{self.get_platform_display()}"

    @property
    def icon_class(self):
        """Return CSS icon class for the platform"""
        return f"icon-{self.platform}"

    @property
    def aria_label(self):
        """Return accessible label for the link"""
        return self.get_platform_display()


@register_setting(icon="site")
class SiteFooterSettings(BaseSiteSetting):
    """
    Site-specific footer settings.
    Points to the active SiteFooter for this site.
    """

    select_related = ["active_footer"]

    active_footer = models.ForeignKey(
        "footer.SiteFooter",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_footer_settings",
        verbose_name="Active Footer",
        help_text="Select the footer to display on this site",
    )

    content_panels = [
        panels.FieldPanel("active_footer"),
    ]

    class Meta:
        verbose_name = "Site Footer"
        verbose_name_plural = "Site Footer"
