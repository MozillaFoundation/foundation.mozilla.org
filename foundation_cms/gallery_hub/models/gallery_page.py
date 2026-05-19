from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.models import Orderable, Page

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.gallery_hub.models.project_page import ProjectPage
from foundation_cms.mixins.hero_image import HeroImageMixin


class FeaturedGalleryProject(Orderable):
    """Orderable child model allowing editors to select up to 25 featured gallery project pages."""

    gallery_page = ParentalKey(
        "gallery_hub.GalleryPage",
        related_name="featured_projects",
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Page,
        related_name="gallery_page_featured_in",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel("project", "gallery_hub.ProjectPage"),
    ]


class GalleryPage(AbstractBasePage, HeroImageMixin):

    lede_text = models.TextField(blank=True)

    body = None

    subpage_types = ["gallery_hub.ProjectPage"]

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("lede_text"),
        MultiFieldPanel(
            [
                InlinePanel("featured_projects", label="Featured Project", max_num=25),
            ],
            heading="Featured Projects",
            classname="collapsible",
        ),
    ]

    class Meta:
        verbose_name = "Gallery Hub Gallery Page"

    template = "patterns/pages/gallery_hub/gallery_page.html"

    @staticmethod
    def _filter_option(tag):
        return {
            "label": tag.name,
            "value": tag.slug,
        }

    @staticmethod
    def _country_filter_option(country):
        return {
            "label": country.name,
            "value": country.code,
        }

    def get_context(self, request):
        context = super().get_context(request)

        featured_project_ids = tuple(
            self.featured_projects.filter(project_id__isnull=False).values_list("project_id", flat=True)
        )
        featured_by_id = {
            page.id: page
            for page in ProjectPage.objects.filter(id__in=featured_project_ids)
            .select_related("expert")
            .prefetch_related(
                "topics",
                "program_label",
            )
        }
        featured = [featured_by_id[project_id] for project_id in featured_project_ids if project_id in featured_by_id]

        topics = sorted(
            {tag.slug: tag for page in featured for tag in page.topics.all()}.values(),
            key=lambda tag: tag.name,
        )
        program_labels = sorted(
            {label.slug: label for page in featured for label in page.program_label.all()}.values(),
            key=lambda label: label.name,
        )
        program_years = sorted(
            {page.program_year for page in featured if page.program_year},
            reverse=True,
        )
        countries = sorted(
            {
                page.expert.location.code: page.expert.location
                for page in featured
                if page.expert and page.expert.location
            }.values(),
            key=lambda country: country.name,
        )

        context["featured_projects"] = featured
        context["filter_categories"] = (
            {
                "key": "topic",
                "options": tuple(self._filter_option(tag) for tag in topics),
                "expanded": True,
            },
            {
                "key": "program",
                "options": tuple(self._filter_option(label) for label in program_labels),
                "expanded": False,
            },
            {
                "key": "year",
                "options": tuple({"label": str(year), "value": str(year)} for year in program_years),
                "expanded": False,
            },
            {
                "key": "country",
                "options": tuple(self._country_filter_option(country) for country in countries),
                "expanded": False,
            },
        )
        context["project_filter_data"] = tuple(
            {
                "id": str(page.id),
                "filters": {
                    "topic": tuple(tag.slug for tag in page.topics.all()),
                    "program": tuple(label.slug for label in page.program_label.all()),
                    "year": (str(page.program_year),) if page.program_year else (),
                    "country": (page.expert.location.code,) if page.expert and page.expert.location else (),
                },
            }
            for page in featured
        )

        return context
