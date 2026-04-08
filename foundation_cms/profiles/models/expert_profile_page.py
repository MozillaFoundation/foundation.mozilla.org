from django.db.models import CASCADE, CharField, TextField, URLField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.profiles.models.abstract_profile_page import AbstractProfilePage


class ExpertExternalLink(TranslatableMixin, Orderable):
    page = ParentalKey(
        "profiles.ExpertProfilePage",
        related_name="external_links",
        on_delete=CASCADE,
    )
    title = CharField(max_length=255, help_text="Title of the external link.")
    description = TextField(blank=True, help_text="Brief description of the link.")
    url = URLField(help_text="Full URL including https://")

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("url"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        TranslatableField("description"),
        SynchronizedField("url"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Expert External Link"
        verbose_name_plural = "Expert External Links"


class ExpertProfilePage(AbstractProfilePage):
    affiliation = CharField(
        max_length=255,
        blank=True,
        help_text="Organization or institution.",
    )

    content_panels = AbstractProfilePage.content_panels + [
        FieldPanel("affiliation"),
        InlinePanel("external_links", label="External Links", max_num=10),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractProfilePage.translatable_fields + [
        TranslatableField("affiliation"),
        TranslatableField("body"),
    ]

    search_fields = AbstractProfilePage.search_fields + [
        index.SearchField("affiliation", boost=3),
    ]

    parent_page_types = ["profiles.ExpertHubPage"]
    subpage_types: list[str] = []

    template = "patterns/pages/profiles/expert_profile_page.html"

    class Meta:
        verbose_name = "Expert Profile Page"
