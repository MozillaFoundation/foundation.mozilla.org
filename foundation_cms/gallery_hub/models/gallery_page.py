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

    def get_context(self, request):
        context = super().get_context(request)

        featured = [
            item.project.specific
            for item in self.featured_projects.select_related("project").all()
            if item.project_id is not None
        ]

        topics = sorted(
            {tag.name for page in featured for tag in page.topics.all()},
        )
        program_labels = sorted(
            {label.name for page in featured for label in page.program_label.all()},
        )
        program_years = sorted(
            {page.program_year for page in featured if page.program_year},
        )

        context["featured_projects"] = featured
        context["filter_topics"] = topics
        context["filter_program_labels"] = program_labels
        context["filter_program_years"] = program_years

        return context
