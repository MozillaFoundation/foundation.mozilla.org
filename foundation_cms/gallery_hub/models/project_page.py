import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, TaggedItemBase
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
=======
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
>>>>>>> main
from wagtail.fields import StreamField
from wagtail.models import Locale
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.blocks.block_registry import BlockRegistry
from foundation_cms.mixins.hero_image import HeroImageMixin


def current_year():
    return datetime.date.today().year


class ProjectPage(AbstractArticlePage, HeroImageMixin):

    cta_link = StreamField(
        BlockRegistry.get_blocks(["link_button_block"]),
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    program_label = ClusterTaggableManager(
        through="gallery_hub.ProjectPageProgramLabel",
        blank=True,
        verbose_name="Program Label",
        help_text=(
            "Add one or more existing program labels. Start typing to search, then press “Down” arrow "
            "on your keyboard to select program label. If program label is unavailable check if it exists by "
            "going to the left side-nav to Snippet > Program Labels > Check if program label exists. "
            "If not, click “Add new program label”."
        ),
    )

    program_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(current_year())],
        default=current_year,
        help_text="Enter a four-digit year.",
    )

<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======
    expert = models.ForeignKey(
        "profiles.ExpertProfilePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gallery_projects",
    )

>>>>>>> main
    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
            classname="collapsible",
        ),
        FieldPanel("lede_text"),
        FieldPanel("cta_link"),
        FieldPanel("program_label"),
        FieldPanel("program_year"),
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======
        PageChooserPanel("expert", "profiles.ExpertProfilePage"),
>>>>>>> main
        FieldPanel("body"),
    ]

    translatable_fields = AbstractArticlePage.translatable_fields + [
        SynchronizedField("hero_image"),
        TranslatableField("hero_image_alt_text"),
        TranslatableField("lede_text"),
        TranslatableField("cta_link"),
        TranslatableField("body"),
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======
        SynchronizedField("expert"),
>>>>>>> main
    ]

    search_fields = AbstractArticlePage.search_fields + [
        index.SearchField("lede_text", boost=6),
        index.SearchField("hero_image_alt_text", boost=2),
    ]

    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Gallery Hub Project Page"

    template = "patterns/pages/gallery_hub/project_page.html"

    # TODO common enough pattern to generalize with other article pages (i.e. NothingPersonalArticlePage)?
    def get_latest_projects(self):
        """
        Returns the 2 latest `Project` objects.
        Uses current locale if available, falls back to default locale.
        """

        current_locale = self.locale
        default_locale = Locale.get_default()

        default_projects = (
            ProjectPage.objects.live()
            .public()
            .filter(locale=default_locale)
            .exclude(id=self.id)
            .order_by("-first_published_at")[:2]
        )

        # Get the best available version for each project
        localized_results = []
        for project in default_projects:
            best_version = project.get_translation(locale=current_locale)
            if best_version and best_version.live:
                localized_results.append(best_version)

        return localized_results

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_projects"] = self.get_latest_projects()
        return context


@register_snippet
class ProgramLabel(TagBase):
    free_tagging = False
    description = models.TextField(blank=True, help_text="Optional program label for a project page.")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Program Label"
        verbose_name_plural = "Program Labels"


class ProjectPageProgramLabel(TaggedItemBase):
    tag = models.ForeignKey(
        ProgramLabel,
        related_name="tagged_projects",
        on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        "gallery_hub.ProjectPage",
        related_name="program_label_items",
        on_delete=models.CASCADE,
    )
