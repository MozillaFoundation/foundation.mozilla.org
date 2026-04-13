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
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
    label = CharField(max_length=255, help_text="Link text.")
    url = URLField(help_text="Full URL including https://")

    panels = [
        FieldPanel("label"),
=======
    title = CharField(max_length=255, help_text="Title of the external link.")
    description = TextField(blank=True, help_text="Brief description of the link.")
    url = URLField(help_text="Full URL including https://")

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
>>>>>>> main
        FieldPanel("url"),
    ]

    translatable_fields = [
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
        TranslatableField("label"),
=======
        TranslatableField("title"),
        TranslatableField("description"),
>>>>>>> main
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
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
    notes = TextField(
        blank=True,
        help_text="Notes for the Web Team.",
    )
=======
>>>>>>> main

    content_panels = AbstractProfilePage.content_panels + [
        FieldPanel("affiliation"),
        InlinePanel("external_links", label="External Links", max_num=10),
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
        FieldPanel("notes"),
=======
>>>>>>> main
        FieldPanel("body"),
    ]

    translatable_fields = AbstractProfilePage.translatable_fields + [
        TranslatableField("affiliation"),
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
        TranslatableField("notes"),
=======
>>>>>>> main
        TranslatableField("body"),
    ]

    search_fields = AbstractProfilePage.search_fields + [
        index.SearchField("affiliation", boost=3),
    ]

<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======
    parent_page_types = ["profiles.ExpertHubPage"]
>>>>>>> main
    subpage_types: list[str] = []

    template = "patterns/pages/profiles/expert_profile_page.html"

    class Meta:
        verbose_name = "Expert Profile Page"
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======

    def get_context(self, request):
        context = super().get_context(request)
        context["gallery_projects"] = self.get_related_projects()

        return context

    def get_related_projects(self):
        return (
            self.gallery_projects.live()
            .public()
            .filter(locale=self.locale)
            .select_related("hero_image")
            .prefetch_related("topics")
        )
>>>>>>> main
