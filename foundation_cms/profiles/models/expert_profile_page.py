from django.db import models
from django.db.models import CASCADE, CharField, TextField, URLField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.models import Orderable, Page, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.gallery_hub.models import ProjectPage
from foundation_cms.profiles.models.abstract_profile_page import AbstractProfilePage
from foundation_cms.utils import localize_queryset

EXPERT_PROFILE_RELATED_CONTENT_LIMIT = 9


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


class ExpertProfileSelectedProject(Orderable):
    page = ParentalKey(
        "profiles.ExpertProfilePage",
        related_name="selected_projects",
        on_delete=CASCADE,
    )
    project = models.ForeignKey(
        Page,
        related_name="expert_profile_project_selections",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel("project", "gallery_hub.ProjectPage"),
    ]


class ExpertProfileSelectedArticle(Orderable):
    page = ParentalKey(
        "profiles.ExpertProfilePage",
        related_name="selected_articles",
        on_delete=CASCADE,
    )
    article = models.ForeignKey(
        Page,
        related_name="expert_profile_article_selections",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel("article"),
    ]


class ExpertProfilePage(AbstractProfilePage):
    affiliation = CharField(
        max_length=255,
        blank=True,
        help_text="Organization or institution.",
    )

    blurb = CharField(
        max_length=115,
        blank=True,
        help_text="Short promotional summary shown in the Expert Hub landing page visualization (max 115 characters).",
    )

    content_panels = AbstractProfilePage.content_panels + [
        FieldPanel("affiliation"),
        FieldPanel("blurb"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "selected_projects",
                    label="Selected Project",
                    max_num=EXPERT_PROFILE_RELATED_CONTENT_LIMIT,
                ),
            ],
            heading="Projects",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "selected_articles",
                    label="Selected Article or Publication",
                    max_num=EXPERT_PROFILE_RELATED_CONTENT_LIMIT,
                ),
            ],
            heading="Articles/Publications",
            classname="collapsible",
        ),
        InlinePanel("external_links", label="External Links", max_num=10),
    ]

    translatable_fields = AbstractProfilePage.translatable_fields + [
        TranslatableField("affiliation"),
        TranslatableField("blurb"),
        SynchronizedField("selected_projects"),
        SynchronizedField("selected_articles"),
        TranslatableField("body"),
    ]

    search_fields = AbstractProfilePage.search_fields + [
        index.SearchField("blurb", boost=5),
        index.SearchField("affiliation", boost=2),
    ]

    parent_page_types = ["profiles.ExpertHubPage"]
    subpage_types: list[str] = []

    template = "patterns/pages/profiles/expert_profile_page.html"

    class Meta:
        verbose_name = "Expert Profile Page"

    def get_context(self, request):
        context = super().get_context(request)
        context["project_block_rows"] = self.get_project_block_rows()
        context["articles"] = self.get_selected_articles()

        return context

    def _get_localized_selected_pages(self, relation_name, page_field_name):
        selected_pages = Page.objects.filter(
            **{
                f"expert_profile_{relation_name}_selections__page": self,
                f"expert_profile_{relation_name}_selections__{page_field_name}_id__isnull": False,
            }
        ).order_by(f"expert_profile_{relation_name}_selections__sort_order")

        return localize_queryset(selected_pages.live().public(), preserve_order=True).specific()

    def get_selected_projects(self):
        return self._get_localized_selected_pages("project", "project")

    def get_selected_articles(self):
        return self._get_localized_selected_pages("article", "article")

    def get_profile_projects(self):
        selected_projects = self.get_selected_projects()
        if selected_projects:
            return selected_projects

        return self.get_related_projects()

    def get_project_block_rows(self):
        project_blocks = [
            {
                "project": project,
                "show_description": True,
            }
            for project in self.get_profile_projects()
        ]

        complete_row_count = len(project_blocks) // 3
        return [project_blocks[index : index + 3] for index in range(0, complete_row_count * 3, 3)]

    def get_related_projects(self):
        return (
            ProjectPage.objects.live()
            .public()
            .filter(expert=self, locale=self.locale)
            .select_related("hero_image")
            .prefetch_related("topics")
            .order_by("-first_published_at", "-id")[:EXPERT_PROFILE_RELATED_CONTENT_LIMIT]
        )
