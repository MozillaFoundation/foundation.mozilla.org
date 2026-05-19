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

    def get_context(self, request):
        context = super().get_context(request)

        featured = [
            item.project.specific
            for item in self.featured_projects.select_related("project").all()
            if item.project_id is not None
        ]

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

        context["featured_projects"] = featured
        context["filter_categories"] = [
            {
                "key": "topic",
                "options": [self._filter_option(tag) for tag in topics],
                "expanded": True,
            },
            {
                "key": "program",
                "options": [self._filter_option(label) for label in program_labels],
                "expanded": False,
            },
            {
                "key": "year",
                "options": [{"label": str(year), "value": str(year)} for year in program_years],
                "expanded": False,
            },
        ]
        context["project_filter_data"] = [
            {
                "id": str(page.id),
                "filters": {
                    "topic": [tag.slug for tag in page.topics.all()],
                    "program": [label.slug for label in page.program_label.all()],
                    "year": [str(page.program_year)] if page.program_year else [],
                },
            }
            for page in featured
        ]

        return context
