from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.models import FoundationMetadataPageMixin


class BaseDonationPage(FoundationMetadataPageMixin, Page):
    class Meta:
        abstract = True


class DonateLandingPage(BaseDonationPage):
    template = "donate/pages/landing_page.html"

    # Only allow creating landing pages at the root level
    parent_page_types = ["wagtailcore.Page"]

    subpage_types: list = []

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        models.PROTECT,
        related_name="+",
    )
    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("featured_image"),
        FieldPanel("intro"),
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
        SynchronizedField("featured_image"),
        TranslatableField("intro"),
    ]
