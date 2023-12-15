from django import forms
from django.core import exceptions
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Locale, Page, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.mozfest import blocks as mozfest_blocks
from networkapi.wagtailpages.models import (
    FoundationBannerInheritanceMixin,
    FoundationMetadataPageMixin,
    Signup,
)
from networkapi.wagtailpages.pagemodels import customblocks
from networkapi.wagtailpages.pagemodels.customblocks.base_fields import base_fields
from networkapi.wagtailpages.utils import (
    get_page_tree_information,
    set_main_site_nav_information,
)


@register_snippet
class Ticket(TranslatableMixin):
    name = models.CharField(
        max_length=100,
        help_text="Identify this ticket for other editors",
    )
    cost = models.CharField(max_length=10, help_text="E.g. €100.00")
    group = models.CharField(max_length=50, help_text="E.g Mega Patrons")
    description = RichTextField(features=["bold", "italic", "ul", "ol"])
    link_text = models.CharField(max_length=25, blank=True, help_text="E.G. Get tickets")
    link_url = models.URLField(blank=True)
    sticker_text = models.CharField(max_length=25, blank=True, help_text="Max 25 characters")

    translatable_fields = [
        TranslatableField("name"),
        TranslatableField("cost"),
        TranslatableField("group"),
        TranslatableField("description"),
        TranslatableField("link_text"),
        SynchronizedField("link_url"),
        TranslatableField("sticker_text"),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        ordering = ["name"]
        verbose_name = "Ticket"

    def clean(self):
        super().clean()

        # If link_url is provided, check if link_text is also provided
        if self.link_url and not self.link_text or self.link_text and not self.link_url:
            raise exceptions.ValidationError("Please provide both link URL and link text, or neither")


class MozfestPrimaryPage(FoundationMetadataPageMixin, FoundationBannerInheritanceMixin, Page):
    header = models.CharField(max_length=250, blank=True)

    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="mozfest_primary_banner",
        verbose_name="Hero Image",
        help_text="Choose an image that's bigger than 4032px x 1152px with aspect ratio 3.5:1",
    )

    intro = RichTextField(help_text="Page intro content", blank=True)

    signup = models.ForeignKey(
        Signup,
        related_name="mozfestpage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose an existing, or create a new, sign-up form",
    )

    body = StreamField(
        base_fields
        + [
            ("session_slider", customblocks.SessionSliderBlock()),
            ("current_events_slider", customblocks.CurrentEventsSliderBlock()),
            ("spaces", customblocks.SpacesBlock()),
            ("tito_widget", customblocks.TitoWidgetBlock()),
            ("tabbed_profile_directory", customblocks.TabbedProfileDirectory()),
            ("newsletter_signup", customblocks.NewsletterSignupBlock()),
            ("statistics", mozfest_blocks.StatisticsBlock()),
            ("carousel_and_text", mozfest_blocks.CarouselTextBlock()),
            ("tickets", mozfest_blocks.TicketsBlock()),
            ("dark_quote", mozfest_blocks.DarkSingleQuoteBlock()),
            ("cta", mozfest_blocks.CTABlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("header"),
        FieldPanel("banner"),
        FieldPanel("intro"),
        FieldPanel("signup"),
        FieldPanel("body"),
    ]

    subpage_types = ["MozfestPrimaryPage", "MozfestLandingPage"]

    show_in_menus_default = True

    use_wide_template = models.BooleanField(
        default=False,
        help_text="Make the body content wide, useful for components like directories",
    )

    settings_panels = Page.settings_panels + [FieldPanel("use_wide_template")]

    structured_data = models.TextField(
        help_text="Structured data JSON for Google search results. Do not include the <script> tag. "
        "See https://schema.org/ for properties and https://validator.schema.org/ to test validity.",
        blank=True,
        null=True,
    )

    promote_panels = FoundationMetadataPageMixin.promote_panels + [
        FieldPanel("structured_data", widget=forms.Textarea(attrs={"rows": 10}))
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("header"),
        SynchronizedField("banner"),
        TranslatableField("intro"),
        # Signup field should be translatable, but is having issues
        # remaining synced across locales. Using sync field as workaround.
        # See also: https://github.com/wagtail/wagtail-localize/issues/648
        SynchronizedField("signup"),
        TranslatableField("body"),
        # Settings tab fields
        SynchronizedField("use_wide_template"),
    ]

    def get_template(self, request):
        if self.use_wide_template:
            return "mozfest/mozfest_primary_page_wide.html"

        return "mozfest/mozfest_primary_page.html"

    @staticmethod
    def _get_signup(name: str, locale: Locale) -> Signup:
        try:
            return Signup.objects.get(name__iexact=name, locale=locale)
        except Signup.DoesNotExist:
            raise Signup.DoesNotExist(
                f"Could not find a 'Signup' object with name '{name}' on locale '{locale.language_code}'"
            )
        except Signup.MultipleObjectsReturned:
            raise Signup.MultipleObjectsReturned(
                f"Found multiple 'Signup' objects with name '{name}' on locale '{locale.language_code}'"
            )

    def get_mozfest_footer(self) -> Signup:
        """Get the Signup object associated with Mozfest for the footer."""
        active_locale = Locale.get_active()
        default_locale = Locale.get_default()
        try:
            mozfest_footer = self._get_signup("mozfest", active_locale)
        except Signup.DoesNotExist:
            mozfest_footer = self._get_signup("mozfest", default_locale)
        return mozfest_footer

    def get_context(self, request, bypass_menu_buildstep=False):
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, "MozfestHomepage")
        context = get_page_tree_information(self, context)

        # primary nav information
        context["menu_root"] = self
        context["menu_items"] = self.get_children().live().in_menu()

        # Also make sure that these pages always tap into the mozfest newsletter for the footer!
        context["mozfest_footer"] = self.get_mozfest_footer()

        if not bypass_menu_buildstep:
            context = set_main_site_nav_information(self, context, "MozfestHomepage")

        return context


class MozfestHomepage(MozfestPrimaryPage):
    """
    MozFest Homepage
    """

    cta_button_label = models.CharField(
        max_length=250,
        blank=True,
        help_text="Label text for the CTA button in the primary nav bar",
    )

    cta_button_destination = models.CharField(
        max_length=2048,
        blank=True,
        help_text="The URL for the page that the CTA button in the primary nav bar should redirect to."
        "E.g., /proposals, https://example.com/external-link",
    )

    # Hero/Banner fields
    banner_heading = models.CharField(
        max_length=250,
        blank=True,
        help_text="A banner heading specific to the homepage",
    )
    banner_meta = models.CharField(
        max_length=50,
        blank=True,
        help_text="Small area above the the banner heading used for dates and meta information.",
    )
    banner_text = models.CharField(
        max_length=150,
        blank=True,
        help_text="Text displayed below the banner heading.",
    )
    banner_link_url = models.URLField(
        max_length=2048,
        blank=True,
        help_text="Link presented to the user as a CTA in the banner.",
    )
    banner_link_text = models.CharField(
        max_length=150,
        blank=True,
        help_text="Text displayed for the banner link.",
    )

    subpage_types = ["MozfestPrimaryPage", "MozfestHomepage", "MozfestLandingPage"]

    # See https://github.com/mozilla/foundation.mozilla.org/issues/7883#issuecomment-996039763
    content_panels = Page.content_panels + [
        FieldPanel("signup"),
        MultiFieldPanel(
            [
                FieldPanel("cta_button_label", heading="Label"),
                FieldPanel("cta_button_destination", heading="Destination"),
            ],
            heading="CTA Button",
        ),
        MultiFieldPanel(
            [
                FieldPanel("banner_heading"),
                FieldPanel("banner"),
                FieldPanel("banner_meta"),
                FieldPanel("banner_text"),
                FieldPanel("banner_link_url"),
                FieldPanel("banner_link_text"),
            ],
            heading="Hero banner",
        ),
        FieldPanel("body"),
    ]

    # Because we inherit from PrimaryPage, but the "use_wide_template" property does nothing
    # we should hide it and make sure we use the right template
    settings_panels = Page.settings_panels

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("cta_button_label"),
        SynchronizedField("cta_button_destination"),
        TranslatableField("banner_heading"),
        SynchronizedField("banner"),
        TranslatableField("banner_meta"),
        TranslatableField("banner_text"),
        SynchronizedField("banner_link_url"),
        TranslatableField("banner_link_text"),
        # Signup field should be translatable, but is having issues
        # remaining synced across locales. Using sync field as workaround.
        # See also: https://github.com/wagtail/wagtail-localize/issues/648
        SynchronizedField("signup"),
        TranslatableField("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        return context

    def get_template(self, request):
        return "mozfest/mozfest_homepage.html"


class MozfestLandingPage(MozfestPrimaryPage):
    # As this class inherits MozfestPrimaryPage, we need to make sure we don't
    # offer the option to have a 'wide template' as it's not supported in the
    # landing page template, so we override the settings_panels property to
    # exclude 'use_wide_template'
    settings_panels = Page.settings_panels

    # Hero/Banner fields
    banner_heading = models.CharField(
        max_length=250,
        blank=True,
        help_text="A banner heading specific to the homepage",
    )
    banner_meta = models.CharField(
        max_length=50,
        blank=True,
        help_text="Small area above the the banner heading used for dates and meta information.",
    )
    banner_text = models.CharField(
        max_length=150,
        blank=True,
        help_text="Text displayed below the banner heading.",
    )
    banner_link_url = models.URLField(
        max_length=2048,
        blank=True,
        help_text="Link presented to the user as a CTA in the banner.",
    )
    banner_link_text = models.CharField(
        max_length=150,
        blank=True,
        help_text="Text displayed for the banner link.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_heading"),
                FieldPanel("banner"),
                FieldPanel("banner_meta"),
                FieldPanel("banner_text"),
                FieldPanel("banner_link_url"),
                FieldPanel("banner_link_text"),
            ],
            heading="Hero banner",
        ),
        FieldPanel("body"),
    ]

    # Because we inherit from PrimaryPage, but the "use_wide_template" property does nothing
    # we should hide it and make sure we use the right template
    settings_panels = Page.settings_panels

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("banner_heading"),
        SynchronizedField("banner_image"),
        TranslatableField("banner_meta"),
        TranslatableField("banner_text"),
        SynchronizedField("banner_link_url"),
        TranslatableField("banner_link_text"),
        TranslatableField("body"),
    ]

    def get_template(self, request):
        return "mozfest/mozfest_landing_page.html"
