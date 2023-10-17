from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, HelpPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import PreviewableMixin, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)
from networkapi.wagtailpages.constants import url_or_query_regex


class DonateBanner(TranslatableMixin, PreviewableMixin, models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Identify this component for editors. This will not be displayed on the banner.",
    )
    title = models.CharField(
        max_length=500,
        help_text="Banner title",
        default="Help Mozilla fight for a better internet this holiday season",
    )
    subtitle = models.CharField(
        max_length=500,
        help_text="Banner subtitle",
        default=(
            "We're proudly nonprofit, working to keep the web healthy. "
            "Your contributions help build a safe and open internet."
        ),
    )
    cta_text = models.TextField(
        help_text="CTA text",
        default="Your contributions help build a safe and open internet. Can you donate today?",
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
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        models.PROTECT,
        related_name="+",
    )

    panels = [
        HelpPanel(content="To enable banner on site, go to Settings > Donate Banner."),
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("cta_text"),
        FieldPanel("cta_button_text"),
        FieldPanel("cta_link"),
        FieldPanel("background_image"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        TranslatableField("subtitle"),
        TranslatableField("cta_text"),
        TranslatableField("cta_button_text"),
        SynchronizedField("cta_link"),
        SynchronizedField("background_image"),
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
            return "Yes"
        return "No"


# Customise DonateBanner Snippet admin listing to show extra columns.
class DonateBannerViewSet(SnippetViewSet):
    model = DonateBanner
    description = "Donate Banner"
    list_display = ["name", "cta_link", "is_active", UpdatedAtColumn()]


register_snippet(DonateBanner, viewset=DonateBannerViewSet)


# Customise chooser to only show the default language banners as options.
# We do not want editors to select the translations as
# localisation will be handled on the template instead.
@hooks.register("register_admin_viewset")
def register_donate_banner_chooser_viewset():
    return DefaultLocaleSnippetChooserViewSet(
        "wagtailsnippetchoosers_custom_donatebanner",
        model=DonateBanner,
        url_prefix="donate_banner/chooser",
    )


@register_setting(icon="pick")
class SiteDonateBanner(BaseSiteSetting):
    select_related = ["active_donate_banner"]

    active_donate_banner = models.ForeignKey(
        "donate_banner.DonateBanner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_donate_banner",
    )

    content_panels = [
        FieldPanel("active_donate_banner"),
    ]

    class Meta:
        verbose_name = "Donate Banner"
