from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.models import Page, PreviewableMixin, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.legacy_apps.wagtailpages.constants import url_or_query_regex


class DonateBanner(TranslatableMixin, PreviewableMixin, models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Identify this component for editors. This will not be displayed on the banner.",
    )
    title = models.CharField(
        max_length=60,
        help_text="Banner title - Recommended max character count of 30",
        default="Help Mozilla fight for a better internet this holiday season",
    )
    subtitle = models.CharField(
        max_length=200,
        help_text="Banner subtitle - Recommended max character count of 60",
        default=(
            "We're proudly nonprofit, working to keep the web healthy. "
            "Your contributions help build a safe and open internet."
        ),
    )
    cta_button_text = models.CharField(
        max_length=500,
        help_text="CTA button text",
        default="Support Mozilla",
    )
    cta_link = models.CharField(
        max_length=255,
        default="?form=donate",
        validators=[
            RegexValidator(
                regex=url_or_query_regex,
                message=(
                    "Please enter a valid URL (starting with http:// or https://), "
                    "or a valid query string starting with ? (Ex: ?form=donate)."
                ),
            ),
        ],
        help_text=(
            "If you would like the CTA button to link to a custom URL, "
            "please enter a valid URL (starting with http:// or https://), "
            "or a valid query string starting with ? (Ex: ?form=donate)."
        ),
    )
    foreground_image = models.ForeignKey(
        "wagtailimages.Image",
        models.PROTECT,
        related_name="+",
    )
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )

    TAILWIND_COLORS = [
        ("tw-bg-red-40", "Red"),
        ("tw-bg-blue-40", "Blue"),
        ("tw-bg-green-10", "Green"),
        ("tw-bg-white", "White"),
        ("tw-bg-black", "Black"),
    ]

    background_color = models.CharField(
        max_length=20,
        choices=TAILWIND_COLORS,
        default="tw-bg-blue-40",
        help_text="Background color for the banner",
        null=True,
        blank=True,
    )

    TEXT_COLORS = [
        ("tw-text-white", "White"),
        ("tw-text-black", "Black"),
    ]

    text_color = models.CharField(
        max_length=20, choices=TEXT_COLORS, default="tw-text-white", help_text="Text color for the banner"
    )

    BUTTON_COLORS = [
        ("tw-bg-blue-40 hover:tw-bg-blue-80", "Blue"),
        ("tw-bg-green-100 hover:tw-bg-green-110", "Green"),
    ]

    button_color = models.CharField(
        max_length=50,
        choices=BUTTON_COLORS,
        default="tw-bg-blue-40 hover:tw-bg-blue-80",
        help_text="Button color for the banner",
    )

    panels = [
        HelpPanel(content="To enable banner on site, visit the DonateBannerPage that is a child of the Homepage."),
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("cta_button_text"),
        FieldPanel("cta_link"),
        FieldPanel("foreground_image"),
        MultiFieldPanel(
            [
                HelpPanel(content="Select either an image or a color to serve as the background for the banner."),
                FieldPanel("background_image"),
                FieldPanel("background_color"),
            ],
            heading="Background",
        ),
        FieldPanel("text_color"),
        FieldPanel("button_color"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        TranslatableField("subtitle"),
        TranslatableField("cta_button_text"),
        SynchronizedField("cta_link"),
        SynchronizedField("foreground_image"),
        SynchronizedField("background_image"),
    ]

    search_fields = [
        index.SearchField("name"),
        index.SearchField("title"),
        index.FilterField("locale_id"),
    ]

    def __str__(self):
        return self.name

    def get_preview_template(self, request, mode_name):
        return "previews/donate_banner.html"

    @admin.display(
        description="Is active? (configure in Settings > Donate Banner)",
    )
    def is_active(self):
        if self.site_donate_banner.exists():
            return True
        return False

    def clean(self):
        super().clean()

        both_selected_error = "Please select either a background image or a background color for the banner."
        none_selected_error = "Please select a background image or a background color for the banner."

        # Validate that either background_image or background_color is set, not both.
        if self.background_image and self.background_color:
            raise ValidationError(
                {
                    "background_image": ValidationError(both_selected_error),
                    "background_color": ValidationError(both_selected_error),
                }
            )
        if not self.background_image and not self.background_color:
            raise ValidationError(
                {
                    "background_image": ValidationError(none_selected_error),
                    "background_color": ValidationError(none_selected_error),
                }
            )


class DonateBannerPage(Page):
    max_count = 1

    donate_banner = models.ForeignKey(
        DonateBanner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_donate_banner",
        help_text=(
            "CTA Banner rendered at the top of the page site-wide. "
            "Note: A/B testing of this banner will also be site-wide and across all locales."
        ),
    )

    content_panels = [
        HelpPanel(
            content=mark_safe(
                "<p>This page is where you can select a <strong>Donate Banner</strong> snippet "
                "and have it render sitewide. Feel free to name the title of this page whatever "
                "you would like, as it's just for use in the CMS only.</p>"
                "<p>To run an <strong>A/B test</strong> between two donate banners, publish this "
                "page with the banner you would like to use as 'control', then select a new donate "
                "banner that you would like to use for your variant, and click "
                "<strong>Save and Create A/B test</strong>.</p>"
                "<p><strong>Note:</strong> Please do not translate this page.</p>"
            )
        ),
        FieldPanel("title", help_text="The page title as you'd like it to be seen in the CMS."),
        MultiFieldPanel(
            [
                FieldPanel("donate_banner"),
            ],
            heading="Donate Banner",
            classname="collapsible",
        ),
    ]

    promote_panels: list = []

    subpage_types: list = []

    parent_page_types = ["wagtailpages.Homepage"]

    template = "previews/donate_banner.html"

    # Override the context for template purposes
    def get_context(self, request):
        context = super().get_context(request)
        context["object"] = self.donate_banner
        return context


@receiver(post_delete, sender=DonateBannerPage)
def delete_all_donate_banner_page_translations(sender, instance, **kwargs):
    """
    Deletes all translated instances of the DonateBannerPage, as they don't auto-delete.
    This prevents lingering aliases from blocking the creation of a new DonateBannerPage
    due to the max_count=1 limit.
    """
    DonateBannerPage.objects.all().delete()
